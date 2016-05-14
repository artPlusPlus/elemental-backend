#!/usr/bin/env bash

if [ $TRAVIS_BRANCH == "master" ]; then
    python ./.ci/anaconda_upload.py "main"
else
    python ./.ci/anaconda_upload.py "dev"
fi
