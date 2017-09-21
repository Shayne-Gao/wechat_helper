d=`date +%Y%m%d` 
common_bin=$(cd -P -- "$(dirname -- "$0")" && pwd -P)
sh ${common_bin}/stop.sh
mv ${common_bin}'/../access.log' ${common_bin}'/../logs/'${d}'.log'
touch ${common_bin}'/../access.log'
echo ${common_bin}/start.sh
