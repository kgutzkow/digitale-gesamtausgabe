#!/bin/bash

export http_proxy="http://192.168.5.200:3128"
export https_proxy="http://192.168.5.200:3128"

git pull --rebase
export PIPENV_VENV_IN_PROJECT=True
yarn config set proxy http://192.168.5.200:3128
yarn config set https-proxy http://192.168.5.200:3128
pipenv install
yarn install
node_modules/.bin/gulp
pipenv run pelican -o output -d content
