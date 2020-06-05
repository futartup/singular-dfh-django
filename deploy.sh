#!/usr/bin/env bash
ROOT_PATH=`pwd`
NGINX_CONFIG_FILE=/etc/nginx/sites-available/anjo-nginx
NGINX_SITES_CONFIG=/etc/nginx/sites-enabled/anjo-nginx.conf
UWSGI_CONFIG_FILE=anjo_uwsgi.ini
echo """
events { 
    worker_connections 1024;
}
http {
  upstream anjo {
    server unix:///tmp/anjo.sock;
  }
  #include /etc/nginx/sites-enabled/*;
  server {
        listen  80;
        server_name anjo.com www.anjo.com;
        charset utf-8;

        # max file upload size
        client_max_body_size 75M;

        # Django media
        location /media {
            alias $ROOT_PATH/media;
        }

        # Static files
        location /static {
            alias $ROOT_PATH/static;
        }

        # Non media requests send to django server
        location / {
            uwsgi_pass anjo;
            include	$ROOT_PATH/uwsgi_params;
            proxy_pass http://jenkins:8080;
            proxy_set_header X-Forwarded-Proto https;
            proxy_set_header Host $http_host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-Host $http_host;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-NginX-Proxy true;
        }
        access_log $ROOT_PATH/dev-nginx-access.log;
        error_log $ROOT_PATH/dev-nginx-error.log;
    }
}
""" > $NGINX_CONFIG_FILE
echo """
# anjo_uwsgi.ini file
[uwsgi]
# Django-related settings
# the base directory (full path)
chdir           = $ROOT_PATH
# Django's wsgi file
module          = anjo.wsgi
# the virtualenv (full path)
home            = $ROOT_PATH/venv
# process-related settings
# master
master          = true
# maximum number of worker processes
processes       = 10
# the socket (use the full path to be safe)
socket          = /tmp/anjo.sock
# ... with appropriate permissions - may be needed
chmod-socket    = 664
# clear environment on exit
vacuum          = true
# create a pidfile
pidfile = /tmp/anjo.pid
# background the process & log
daemonize = uwsgi.log
""" > $UWSGI_CONFIG_FILE
if [ ! -d "$NGINX_SITES_CONFIG" ]; then
    mkdir -p "$NGINX_SITES_CONFIG"
fi
ln -sf $NGINX_CONFIG_FILE /etc/nginx/sites-enabled