#!/usr/bin/env bash
set -e # halt script on error

JEKYLL_ENV=production bundle exec jekyll build --destination site --trace
bundle exec htmlproofer ./site --disable-external # Dont check external links