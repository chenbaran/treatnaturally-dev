release: python manage.py migrate
web: gunicorn treatnaturallystore.wsgi
worker: celery -A treatnaturallystore worker