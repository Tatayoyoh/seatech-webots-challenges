#!/bin/bash

for ACCOUNT in $(cat students2022-githubs.list); do
    if [ ! -d $ACCOUNT ] ; then
      REPOSITORY="seatech-poo-python-robotic"

      # check if repository exists
      curl -s https://api.github.com/repos/$ACCOUNT/seatech-poo-python-robotic | grep -iq 'Not Found'
      if [ "$?" == "0" ] ; then
        # avec un 's' !! :O
        REPOSITORY="seatech-poo-python-robotics"
      fi

      REMOTE="https://github.com/$ACCOUNT/$REPOSITORY.git"
      echo "git clone $REMOTE $ACCOUNT" 
      git clone $REMOTE $ACCOUNT
    fi
done
