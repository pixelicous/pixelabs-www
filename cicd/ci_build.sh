#!/usr/bin/env bash
set -e # halt script on error
python ./tools/litter_cleaner.py

JEKYLL_ENV=production bundle exec jekyll build --destination site --trace
bundle exec htmlproofer ./site --disable-external

# Enabled during debug
# bundle exec jekyll clean