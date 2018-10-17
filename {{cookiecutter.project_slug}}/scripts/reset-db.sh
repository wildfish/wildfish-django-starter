cd `dirname $0`/..
python manage.py reset_db --noinput
python manage.py migrate --noinput
