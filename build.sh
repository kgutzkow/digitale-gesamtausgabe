#!/bin/bash

export http_proxy="http://192.168.5.200:3128"
export https_proxy="http://192.168.5.200:3128"

# The local-config file can be used to set deployment-specific environment settings, such as proxies
if [ -f 'local-config' ]
then
    source local-config
fi

# Run optional pre-build scripts
if [ -f 'pre-build' ]
then
    ./pre-build
fi

# Fetch all remote branches
git checkout master -- .
for remote in `git branch -r | grep -v '\->'`; do git branch --track ${remote#origin/} $remote; done
git pull --all

# Build the main site
export PIPENV_VENV_IN_PROJECT=True
pipenv install
yarn install
node_modules/.bin/gulp
pipenv run pelican -o output -d content

# Build the branch-specific preview sites
for branch in `git branch | grep -v '* master'`; do git checkout $branch; node_modules/.bin/gulp; pipenv run pelican -o output/preview/$branch content; done

# Get us back to the master branch
git checkout master

# Run optional post-build scripts
if [ -f 'post-build' ]
then
    ./post-build
fi
