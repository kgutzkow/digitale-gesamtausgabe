#!/bin/bash

git pull --rebase
pipenv install
npm install
gulp
pipenv run pelican -o output -d content
