web: gunicorn app.main.wsgi:application --pythonpath=app
release: ./app/manage.py collectstatic --noinput ; ./app/manage.py migrate
