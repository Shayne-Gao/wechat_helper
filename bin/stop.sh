ps -ef |grep manage.py| grep runserver| cut -c 9-15|xargs kill -9
