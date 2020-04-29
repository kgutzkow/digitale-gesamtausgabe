#!/bin/bash

# Ensure only on copy of the script runs at any time
exec 100>.build.lock || exit 1
flock -w 300 100 || exit 1
trap 'rm -f .build.lock' EXIT

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

git checkout -f master

# Fetch all remote branches
if [ -f 'branches.txt' ]
then
    cat branches.txt | while read branch
    do
        if [ -n "$branch" ]
        then
            git branch -r | grep $branch
            if [ $? -eq 0 ]
            then
                git branch | grep $branch
                if [ $? -ne 0 ]
                then
                    git branch --track $branch origin/$branch
                fi
            fi
        fi
    done
fi
git pull --all

# Build the main site
poetry install
yarn install --frozen-lockfile --check-files --non-interactive
node_modules/.bin/gulp
poetry run pelican -s publishconf.py -o output -d content

# Build the branch-specific preview sites
if [ -f 'branches.txt' ]
then
    cat branches.txt | while read branch
    do
        if [ -n "$branch" ]
        then
            git branch | grep $branch
            if [ $? -eq 0 ]
            then
                git checkout $branch;
                git pull
                poetry install
                yarn install --frozen-lockfile --check-files --non-interactive
                node_modules/.bin/gulp
                poetry run pelican -s publishconf.py -o output/preview/$branch -d content
            fi
        fi
    done
fi

# Get us back to the master branch
git checkout -f master

# Run optional post-build scripts
if [ -f 'post-build' ]
then
    source post-build
fi
