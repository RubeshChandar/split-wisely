#! /bin/sh

git add .
# echo "Enter a custom message"
# read msg
git cm "$1"
git push

# A custom bash file to save some time in pushing changes to git