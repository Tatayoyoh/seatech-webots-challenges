import os
import sys
import shutil

""" repo-list file should look like :
https://github.com/username1/seatech-python-robotic.git 
https://github.com/username2/seatech-python-robotic.git 
https://github.com/username3/seatech-python-robotic.git
No trailing blank line !
"""

PICK_AMOUNT = 3
CURRENT_FOLDER = os.path.dirname(__file__)
REPO_LIST_FILE = os.path.join(CURRENT_FOLDER, 'repo-list')
REPO_FOLDER = os.path.join(CURRENT_FOLDER, 'challengers')
GENERIC_CONTROLLER_NAME = 'my_controller'

if __name__ == '__main__':
    with open(REPO_LIST_FILE, 'r') as f:
        repos = f.read()

    repos = repos.split('\n')

    if '--rm' in sys.argv and os.path.exists(REPO_FOLDER):
        shutil.rmtree(REPO_FOLDER)

    if not os.path.exists(REPO_FOLDER):
        os.mkdir(REPO_FOLDER)

    for repo in repos:
        os.chdir(REPO_FOLDER)
        username = repo.split('/')[3]
        print('CHECK', username)
        if not os.path.exists(username):
            os.system('git clone %s %s'%(repo, username))
            os.chdir(username)
        else:
            os.chdir(username)
            os.system('git pull')

        for root, dirs, files in os.walk("."):
            if GENERIC_CONTROLLER_NAME in dirs:
                dest = os.path.join(CURRENT_FOLDER, 'controllers', '%s_%s'%(GENERIC_CONTROLLER_NAME, username))
                if os.path.exists(dest):
                    shutil.rmtree(dest)
                shutil.copytree(os.path.join(root, GENERIC_CONTROLLER_NAME), dest)
                print('OK copied')

    os.chdir(CURRENT_FOLDER)