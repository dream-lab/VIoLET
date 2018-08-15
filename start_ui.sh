#!/usr/bin/env bash

python backend_ui.py;

pushd ./ui/violet/dist; python -m SimpleHTTPServer 4000; popd
