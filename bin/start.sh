common_bin=$(cd -P -- "$(dirname -- "$0")" && pwd -P)
d=`date +%Y%m%d`
nohup python -u ${common_bin}/../manage.py runserver 0.0.0.0:80 >>${common_bin}/../logs/${d}.log & 


