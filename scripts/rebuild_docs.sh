rm docs/*.rst
rm -rf builddocs/
sphinx-apidoc src/ormex --full -o docs -H 'django-ormex' -A 'Artur Barseghyan <artur.barseghyan@gmail.com>' -V '0.1' -f -d 20
cp docs/conf.distrib docs/conf.py
