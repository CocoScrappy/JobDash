#web: gunicorn django_config.wsgi
# web: daphne <application>.asgi:application --port $PORT --bind 0.0.0.0

web: daphne django_config.asgi:application --port $PORT --bind 0.0.0.0 -v2
#worker: python manage.py runworker -v2


release: python manage.py makemigrations --noinput
release: python manage.py collectstatic --noinput
release: python manage.py migrate --noinput