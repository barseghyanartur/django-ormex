wget -O django_ormex_demo_installer.tar.gz https://github.com/barseghyanartur/django-ormex/archive/stable.tar.gz
virtualenv django-ormex
source django-ormex/bin/activate
mkdir django_ormex_demo_installer/
tar -xvf django_ormex_demo_installer.tar.gz -C django_ormex_demo_installer
cd django_ormex_demo_installer/django-ormex-stable/examples/simple/
pip install -r ../../requirements.txt
pip install https://github.com/barseghyanartur/django-ormex/archive/stable.tar.gz
mkdir ../media/
mkdir ../media/static/
mkdir ../static/
mkdir ../db/
mkdir ../logs/
mkdir ../tmp/
cp settings/local_settings.example settings/local_settings.py
./manage.py migrate --noinput --traceback -v 3
./manage.py collectstatic --noinput --traceback -v 3
./manage.py books_create_test_data --number=100 --traceback -v 3
./manage.py runserver 0.0.0.0:8001 --traceback -v 3
