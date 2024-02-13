from os.path import join, exists, dirname
from os import rename, chdir, mkdir, system, walk
import sys
from shutil import rmtree, copytree

""" repo-list file should look like :
https://github.com/username1/seatech-python-robotic.git 
https://github.com/username2/seatech-python-robotic.git 
https://github.com/username3/seatech-python-robotic.git
No trailing blank line !
"""

PICK_AMOUNT = 3
CURRENT_FOLDER = dirname(__file__)
REPO_LIST_FILE = join(CURRENT_FOLDER, 'repo-list')
REPO_FOLDER = join(CURRENT_FOLDER, 'teams')
GENERIC_CONTROLLER_NAME = 'my_controller'

if __name__ == '__main__':
    with open(REPO_LIST_FILE, 'r') as f:
        repos = f.read()

    repos = repos.split('\n')

    if '--rm' in sys.argv and exists(REPO_FOLDER):
        rmtree(REPO_FOLDER)

    if not exists(REPO_FOLDER):
        mkdir(REPO_FOLDER)

    for repo in repos:
        chdir(REPO_FOLDER)
        username = repo.split('/')[3]
        print('CHECK', username)
        if not exists(username):
            system('git clone %s %s'%(repo, username))
            chdir(username)
        else:
            chdir(username)
            system('git pull')

        for root, dirs, files in walk("."):
            if GENERIC_CONTROLLER_NAME in dirs:
                new_controller_name = '%s_%s'%(GENERIC_CONTROLLER_NAME, username)
                dest = join(CURRENT_FOLDER, 'controllers', new_controller_name)
                if exists(dest):
                    rmtree(dest)
                copytree(join(root, GENERIC_CONTROLLER_NAME), dest)
                rename(join(dest, 'my_controller.py'), join(dest, new_controller_name+'.py'))
                print('OK copied')

    chdir(CURRENT_FOLDER)