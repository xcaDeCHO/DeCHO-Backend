release: python manage.py makemigrations
release: python manage.py migrate

web: gunicorn Decho.wsgi --log-file -