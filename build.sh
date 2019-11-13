#!/bin/bash

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
cat branches.txt | while read branch
do
    git branch --track $branch origin/$branch
done
git pull --all

# Build the main site
export PIPENV_VENV_IN_PROJECT=True
pipenv install
yarn install
node_modules/.bin/gulp
pipenv run pelican -o output -d content

# Build the branch-specific preview sites
cat branches.txt | while read branch
do
    git checkout $branch;
    node_modules/.bin/gulp
    pipenv run pelican -o output/preview/$branch -d content
done

# Get us back to the master branch
git checkout master -- .

# Run optional post-build scripts
if [ -f 'post-build' ]
then
    ./post-build
fi
