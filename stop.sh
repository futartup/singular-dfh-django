#!/usr/bin/env bash
# shut down uwsgi
uwsgi --stop /tmp/anjo.pid
# gracefully stop nginx
sudo nginx -s stop