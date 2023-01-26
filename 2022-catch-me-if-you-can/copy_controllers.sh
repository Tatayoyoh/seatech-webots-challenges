#!/bin/bash

FIND_PATH="students_repos"

for repo in $(ls -1 $FIND_PATH); do
    repo_path="$FIND_PATH/$repo"
    if [ -d $repo_path ] && [ -d $repo_path/.git ] ; then
      NEW_CONTROLLER_PATH="controllers/${repo}_controller"
      find $repo_path -name '*_controller' | xargs -I {} cp -R {} $NEW_CONTROLLER_PATH
      if [ -d $NEW_CONTROLLER_PATH ] ; then
        echo -e "Copy '$repo' controller to $NEW_CONTROLLER_PATH"
        for FILE in $(find $NEW_CONTROLLER_PATH -name "*_controller.py") ; do 
          DIR=`dirname ${FILE}`
          echo -e "\tmv $FILE $DIR/${repo}_controller.py" 
          mv $FILE $DIR/${repo}_controller.py
        done
      else
        echo "WARNING: no 'controllers' folder found in '$repo' repo"
      fi
    fi
done
