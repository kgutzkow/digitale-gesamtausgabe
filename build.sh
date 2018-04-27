#!/bin/bash

pipenv install
npm install
gulp
pipenv run pelican -o output -d content
