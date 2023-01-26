#!/bin/bash

base=$(pwd)
for repo in $(ls -1); do
    if [ -d $repo ] && [ -d $repo/.git ] ; then
      echo -e "Remove folder \e[1m\e[34m$repo\e[0m"
      rm -Rf $repo
    fi
done
