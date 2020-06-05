#!/usr/bin/env bash
# start nginx
sudo nginx
# start uwsgi
uwsgi --ini anjo_uwsgi.ini