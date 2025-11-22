#!/bin/bash
set -e

# Build the project
npm run build

# Navigate into the build output directory
cd dist

# Initialize a new git repository
git init
git checkout -b gh-pages

# Add all files
git add -A

# Commit
git commit -m "deploy"

# Push to the gh-pages branch
# Using the remote URL from the parent repo would be better, but hardcoding for now based on previous context
git push -f https://github.com/aniketink/anxiety_porfolio.git gh-pages

cd -
