#!/bin/bash

git add .github/workflows/ci-cd.yml
git add .github/workflows/crawler_buildspec_S3.yml
git commit -m "Move workflow file to correct location"
git push origin main
