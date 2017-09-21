common_bin=$(cd -P -- "$(dirname -- "$0")" && pwd -P)
sh ${common_bin}/stop.sh


sh ${common_bin}/start.sh
