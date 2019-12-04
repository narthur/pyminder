#!/bin/bash

PIPV=$(pip search "pyminder")
LINE=$(cat setup.py | grep -i version)
VERSION=$(echo $LINE | cut -d'"' -f2)

if [[ "$PIPV" == *"$VERSION"* ]] ; then
  echo 'Version has not been bumped'
  exit 1
fi

echo "New version: $VERSION"

pip install twine wheel
python setup.py sdist bdist_wheel
tar tzf "dist/pyminder-$VERSION.tar.gz"
twine check dist/*
twine upload dist/*
