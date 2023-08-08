#!/bin/bash
cd /var/www/gr/
source gr/bin/activate

exec /var/www/gr/gr/bin/gunicorn --timeout 600 --access-logfile - --workers 3 --bind unix:/run/gunicorn.sock wsgi:application