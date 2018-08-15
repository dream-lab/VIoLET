#!/usr/bin/env bash

backend="python backend_ui.py";

frontend="python -m SimpleHTTPServer 4000";

$backend &

pushd ./ui/violet/dist;

$frontend &

popd;
