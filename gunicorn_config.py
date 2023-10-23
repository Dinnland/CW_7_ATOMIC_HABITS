command = '/root/code/mysite/env/bin/gunicorn'
pythonpath = '/usr/bin/python3'
bind = '0.0.0.0:8000'
workers = 3
User = 'root'
limit_request_fields = 32000
limit_request_field_size = 0
raw_env = 'DJANGO_SETTINGS_MODULE=main.settings'
