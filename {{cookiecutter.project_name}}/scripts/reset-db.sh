cd `dirname $0`/..
rm dev.sqlite
python manage.py syncdb --noinput
