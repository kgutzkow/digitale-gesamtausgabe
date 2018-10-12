#!/bin/bash

git pull --rebase
export PIPENV_VENV_IN_PROJECT=True
pipenv install
npm install
node_modules/.bin/gulp
pipenv run pelican -o output -d content
