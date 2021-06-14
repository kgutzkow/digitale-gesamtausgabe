#!/bin/bash

# Ensure only on copy of the script runs at any time
exec 100>.build.lock || exit 1
flock -w 300 100 || exit 1
trap 'rm -f .build.lock' EXIT

echo "=================="
echo "Preparing to build"
echo "=================="
echo

# The local-config file can be used to set deployment-specific environment settings, such as proxies
if [ -f 'local-config' ]
then
    source local-config
fi

# Run optional pre-build scripts
if [ -f 'pre-build' ]
then
    source pre-build
fi

echo "========================"
echo "Fetching the latest data"
echo "========================"
echo

rm -rf theme/static/css theme/static/js theme/static/reader

git checkout -f default
git pull

# Build the main site
echo
echo "================="
echo "Building the site"
echo "================="
echo

poetry install --no-dev
poetry run pelican -s publishconf.py -o output -d content

echo
echo "==============="
echo "Build completed"
echo "==============="
echo

# Run optional post-build scripts
if [ -f 'post-build' ]
then
    source post-build
fi
