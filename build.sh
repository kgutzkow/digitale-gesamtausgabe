#!/bin/bash

git pull --rebase
pipenv install
npm install
node_modules/.bin/gulp
pipenv run pelican -o output -d content
