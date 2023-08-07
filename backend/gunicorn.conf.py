import os

chdir = "/backend/"
bind = ":8000"
workers = 4
timeout = 1800
reload_engine = 'poll'
reload = True
reload_extra_files = [
    "/backend/templates/",
    "/backend/templates/accounts",
    "/backend/templates/messages",
    "/backend/templates/events",
    "/backend/static/js",
]

# Logging
errorlog = '/var/log/django/gunicorn_error.log'
accesslog = '/var/log/django/gunicorn_access.log'
access_log_format = '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s" "%({X-Real-IP}i)s" "%({X-Forwarded-For}i)s"'
loglevel = os.getenv('GUNICORN_LOG_LEVEL', 'info')