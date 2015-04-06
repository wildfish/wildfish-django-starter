cd `dirname $0`/..
rm db.sqlite3
python manage.py syncdb --noinput
