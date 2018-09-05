#!/usr/bin/env bash

backend="gunicorn --bind 0.0.0.0:5000 -t 600 backend_wsgi";

frontend="python -m SimpleHTTPServer 80";

pushd ..;

$backend &

popd;

pushd ./violet/dist;

$frontend &

popd;
