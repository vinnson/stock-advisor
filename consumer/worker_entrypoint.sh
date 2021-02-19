cd /srv
pip install -r requirements.txt
celery -A pull worker --logfile=/dev/null
# celery -A pull worker --loglevel=info
