#!/usr/bin/env bash

backend="gunicorn --bind 0.0.0.0:5000 -t 600 backend_wsgi";

frontend="python -m SimpleHTTPServer 80";

$backend &

pushd ./ui/violet/dist;

$frontend &

popd;
