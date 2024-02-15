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

if __name__ == '__main__':
    with open(REPO_LIST_FILE, 'r') as f:
        repos = f.read()

    repos = repos.split('\n')

    if '--rm' in sys.argv and exists(REPO_FOLDER):
        rmtree(REPO_FOLDER)

    if not exists(REPO_FOLDER):
        mkdir(REPO_FOLDER)

    for repo in repos:
        if not repo.strip(): # blank line
            continue
        
        chdir(REPO_FOLDER)
        team_name = repo.split(' ')[1]
        print('CHECK', team_name)
        if not exists(team_name):
            system('git clone %s'%(repo))
            chdir(team_name)
        else:
            chdir(team_name)
            system('git pull')


    chdir(CURRENT_FOLDER)