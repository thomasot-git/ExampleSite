#!/bin/sh

echo "--- Installing dependencies ---"
#pip3 install -U git+https://github.com/OrganicIrradiation/scholarly.git

echo "--- Extracting Scholar data ---"
#python bin/generatescholar.py
python bin/generatediva.py

echo "--- Saving Scholar json on data folder ---"
#mkdir -p data
#mv publications.json data/

#git config user.email "thomas.ohlsontimoudas@gmail.com/"
#git config user.name "thomasot-git"
#git clone https://github.com/thomasot-git/Personal-webpage/ private
#git status
#git add data/publications.json
#git status
#git commit -m 'publications' -- data/publications.json
#git push -f -q https://$GITHUB_TOKEN@github.com/thomasot-git/Personal-webpage/ master