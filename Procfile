release: python manage.py migrate

web: gunicorn Decho.wsgi --log-file -

worker: python manage.py run_huey