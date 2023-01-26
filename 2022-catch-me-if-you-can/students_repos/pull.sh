#!/bin/bash

base=$(pwd)
for repo in $(ls -1); do
    if [ -d $repo ] && [ -d $repo/.git ] ; then
      echo -e "Pulling \e[1m\e[34m$repo\e[0m"
      cd $base/$repo
      git pull
      cd $base
    fi
done

cd $base
