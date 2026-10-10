#!/usr/bin/env bash
# quota-gate.sh — décision GO / STOP déterministe de la skill gquota (aucun raisonnement modèle).
#
# Usage :
#   quota-gate.sh sid
#       → affiche l'id de session à passer à list_events (session_<suffixe>)
#   quota-gate.sh check <u5h> <u7d> <reset7d>
#       u5h, u7d : unifiedWindows.five_hour / seven_day .utilization (fraction 0-1, telle que lue)
#       reset7d  : unifiedWindows.seven_day.resetsAt (epoch, secondes)
#
# Sortie : une ligne « GO … » (exit 0) ou « STOP … » (exit 1).
# Donnée absente ou invalide → STOP (décision quotaKOA : prudence).
# Test : QG_NOW=<epoch> simule l'heure courante.
#
# Règles (décisions Guillaume 2026-10-09, détail dans SKILL.md) :
#   - semaine = du reset hebdo Anthropic (vendredi 21h Paris) au suivant ;
#   - jours révolus = nombre de passages à l'heure du reset (21h) depuis le début de semaine, sans prorata ;
#   - seuil = jours × 100/7 − 10 (tauxB) ; GO si hebdo < seuil ;
#   - STOP si hebdo > 80 % ou si fenêtre 5 h > 80 % (sess5hA) ;
#   - fenêtre burn = 30 min avant le reset (20h30-20h59) : seuil et plafond 80 % ignorés,
#     fenêtre 5 h toujours vérifiée (fenBurnA) ; STOP dur 1 min avant le reset (20h59) ;
#   - jour du reset (vendredi, de 00h00 heure de Paris à l'ouverture de la fenêtre burn) :
#     seuil et plafond hebdo portés à 90 % (fin90A), pour viser ~90 % consommés par semaine
#     en laissant au moins 10 % à Guillaume pour sa journée du vendredi.

set -u

TZ_LOCAL="Europe/Paris"
TAUX="100/7"        # % de quota hebdo par jour révolu
MARGE=10            # marge retirée au seuil
PLAFOND_HEBDO=80
CIBLE_FIN=90        # seuil et plafond hebdo du jour du reset (fin90A)
PLAFOND_5H=80
FENETRE_BURN=1800   # début de la fenêtre burn, en secondes avant le reset (20h30)
COUPURE=60          # STOP dur, en secondes avant le reset (20h59)

stop() { echo "STOP motif=\"$1\"${2:+ $2}"; exit 1; }
go()   { echo "GO motif=\"$1\"${2:+ $2}"; exit 0; }

case "${1:-}" in
  sid)
    sid="${CLAUDE_CODE_REMOTE_SESSION_ID:-}"
    [ -n "$sid" ] || stop "pas en session cloud (CLAUDE_CODE_REMOTE_SESSION_ID vide)"
    echo "session_${sid#*_}"
    exit 0
    ;;
  check) ;;
  *) stop "usage : quota-gate.sh sid | check <u5h> <u7d> <reset7d>" ;;
esac

[ $# -eq 4 ] || stop "check attend 3 valeurs, reçu $(($# - 1))"
u5h=$2; u7d=$3; reset=$4
num='^[0-9]+([.][0-9]+)?$'
[[ $u5h =~ $num && $u7d =~ $num ]] || stop "utilization illisible (5h=$u5h hebdo=$u7d)"
[[ $reset =~ ^[0-9]{9,11}$ ]] || stop "resetsAt hebdo illisible ($reset)"

now=${QG_NOW:-$(date +%s)}
p5=$(awk -v u="$u5h" 'BEGIN{printf "%.1f", u*100}')
p7=$(awk -v u="$u7d" 'BEGIN{printf "%.1f", u*100}')
reset_txt=$(TZ=$TZ_LOCAL date -d "@$reset" '+%d/%m %H:%M')
etat="hebdo=${p7}% 5h=${p5}% reset=\"$reset_txt\""

gt() { awk -v a="$1" -v b="$2" 'BEGIN{exit !(a > b)}'; }
lt() { awk -v a="$1" -v b="$2" 'BEGIN{exit !(a < b)}'; }

[ "$now" -lt "$reset" ] || stop "données périmées (reset hebdo déjà passé)" "$etat"

# Jours révolus : passages à l'heure locale du reset (21h) depuis le début de semaine,
# calculés en heure de Paris pour rester justes au changement d'heure.
rdate=$(TZ=$TZ_LOCAL date -d "@$reset" '+%F')
rtime=$(TZ=$TZ_LOCAL date -d "@$reset" '+%H:%M:%S')
borne() { TZ=$TZ_LOCAL date -d "$(date -d "$rdate $1 days" +%F) $rtime" +%s; }
[ "$now" -ge "$(borne -7)" ] || stop "données incohérentes (maintenant avant le début de semaine)" "$etat"
jours=0
for k in 1 2 3 4 5 6; do
  [ "$now" -ge "$(borne $((k - 7)))" ] && jours=$k
done

# Fenêtre de fin de semaine (vendredi 20h30-20h59), puis coupure à 20h59.
if [ "$now" -ge $((reset - COUPURE)) ]; then
  stop "coupure de fin de semaine (1 min avant le reset)" "$etat"
fi
if [ "$now" -ge $((reset - FENETRE_BURN)) ]; then
  gt "$p5" "$PLAFOND_5H" && stop "fenêtre 5 h > ${PLAFOND_5H} %" "$etat"
  fin=$(TZ=$TZ_LOCAL date -d "@$((reset - COUPURE))" '+%H:%M')
  go "fenêtre burn de fin de semaine, arrêt impératif à $fin" "$etat fin=$fin"
fi

# Jour du reset (fin90A) : depuis minuit heure de Paris, seuil et plafond à CIBLE_FIN.
if [ "$now" -ge "$(TZ=$TZ_LOCAL date -d "$rdate 00:00:00" +%s)" ]; then
  seuil="$CIBLE_FIN.0"; plafond=$CIBLE_FIN
  etat="$etat seuil=${seuil}% jours=$jours dernier_jour"
else
  seuil=$(awk -v j="$jours" -v m="$MARGE" "BEGIN{printf \"%.1f\", j*$TAUX - m}")
  plafond=$PLAFOND_HEBDO
  etat="$etat seuil=${seuil}% jours=$jours"
fi

gt "$p5" "$PLAFOND_5H" && stop "fenêtre 5 h > ${PLAFOND_5H} %" "$etat"
gt "$p7" "$plafond" && stop "hebdo > ${plafond} %" "$etat"
lt "$p7" "$seuil" && go "reliquat des jours révolus disponible" "$etat"
stop "hebdo >= seuil des jours révolus" "$etat"
