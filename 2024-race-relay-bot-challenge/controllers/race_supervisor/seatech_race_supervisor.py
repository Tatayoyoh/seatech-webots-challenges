from os.path import abspath, dirname, join, exists
from os import listdir, walk
from pprint import pprint
import random
import math
from controller import Supervisor, Robot
from webots_parser import WebotsParser
import pyjq
import shutil
import os
import pathlib

# SLOT_QUERY = '.root[0].fields[] | select(.name == $robotname).value.fields[] | select(.name | test(".*slot";"i"))'
SLOT_QUERY = '.root[].fields[] | select(.name | test(".*slot";"i"))'

ROBOT_LIST = [
    'Fabtino',
    'SickS300',
    'TurtleBot3Burger',
    'RobotisLds01',
    'Rosbot',
    'E-puck',
    'HokuyoUrg04lxug01',
    'SummitXlSteel',
    'Tiago++',
    'Robotino3',
    'Robotino3Platform',
    'Pioneer3at',
    'Koala',
    'Create',
    'Pr2',
    'Thymio2',
    'Khepera3'
]

class Team():
    def __init__(self, name, repo_path):
        self.name: str = name
        self.repo_path = repo_path
        self.challengers: list[Challenger] = []
        self.unsuported_challengers: list[Challenger] = []

    def __repr__(self) -> str:
        return self.name

    def __str__(self) -> str:
        return self.__repr__()


class Challenger():

    def __init__(self, name, src_path):
        self.name = name
        self.src_path = src_path
        self.robot = ''
        self.controller = ''
        self.world = None
        self.robot_settings = []
        self.simu_DEF = None

    def __repr__(self) -> str:
        return '%s (%s): %s %s [%s]' % (self.name, self.src_path, self.robot, self.controller, self.robot_settings)

    def __str__(self) -> str:
        return self.__repr__()


class SeatechRaceSupervisor(Supervisor):
    def __init__(self, test_mode=False):
        if not test_mode:
            super().__init__()
        # 'teams' folder is created by 'fetch_teams_repositories.py' script
        self.__timestep = int(self.getBasicTimeStep())
        self.__controllers_folder = abspath(
            join(dirname(abspath(__name__)), '..'))
        self.__teams_folder = abspath(
            join(dirname(abspath(__name__)), '../../teams'))
        self.__teams: list[Team] = []
        self.__selected_team: Team = None
        self.__challengers = []
        self.__unsuported_challengers = []
        self.__running = False

        self.__fetch_teams()

    @property
    def timestep(self):
        return self.__timestep

    @property
    def teams(self) -> list[Team]:
        return self.__teams
    
    @property
    def selected_team(self) -> Team:
        return self.__selected_team

    @property
    def challengers(self):
        return self.__challengers

    @property
    def unsuported_challengers(self):
        return self.__unsuported_challengers

    @property
    def running(self):
        return self.__running

    def __get_used_robot(self, proto_content):
        for r in ROBOT_LIST:
            if r in proto_content:
                return r
        return None

    def __fetch_teams(self):
        for team_name in listdir(self.__teams_folder):
            self.__teams.append(
                Team(team_name, join(self.__teams_folder, team_name)))

    def select_team(self, index):
        self.__selected_team = self.teams[index]

    def fetch_challengers_robots(self):
        self.__selected_team.challengers = []
        self.__selected_team.unsuported_challengers = []

        # fetch folder
        for root, dirs, files in walk(self.__selected_team.repo_path):
            if 'worlds' in dirs and 'controllers' in dirs:
                print(root, dirs)
                challenger_world_file = join(
                    root, 'worlds', '2024-simu_project.wbt')
                for controller_name in listdir(join(root, 'controllers')):
                    controller_path = join(
                        root, 'controllers', controller_name)

                    challenger = Challenger(
                        name=controller_name,
                        src_path=controller_path
                    )

                    if exists(controller_path) and exists(challenger_world_file):
                        # get robot controller name
                        challenger.controller = self.__selected_team.name+'_'+controller_name

                        # parse Webots PROTO file
                        try:
                            proto = WebotsParser()
                            proto.load(challenger_world_file)

                            controller_copy = join(self.__controllers_folder, challenger.controller)
                            if exists(controller_copy):
                                shutil.rmtree(controller_copy)
                            shutil.copytree(controller_path, controller_copy)
                            shutil.move(join(controller_copy,controller_name+'.py'), join(controller_copy,challenger.controller+'.py'))
                        except Exception as e:
                            print('ERROR', str(challenger))
                            print(e)
                            break

                        # get robot World
                        challenger.world = challenger_world_file
                        # get robot Name
                        challenger.robot = self.__get_used_robot(str(proto.content))
                        # get robot Slots
                        robot_slots = pyjq.all(SLOT_QUERY, proto.content)

                        for slot in robot_slots:
                            with open('/tmp/slots', 'w', newline='\n') as proto.file:
                                proto._write_field(slot)
                            with open('/tmp/slots', 'r') as proto.file:
                                proto_content = proto.file.read()
                                challenger.robot_settings.append(proto_content.replace('\n', ''))

        if challenger.robot and challenger.controller:
            self.__selected_team.challengers.append(challenger)
        else:
            self.__selected_team.unsuported_challengers.append(challenger)

        print('IMPORTED', len(self.__selected_team.challengers))
        print('IGNORED', self.__selected_team.unsuported_challengers)

    def clear(self):
        for challenger in self.__selected_team.challengers:
            challenger.simu_DEF.remove()
            challenger.simu_DEF = None

        self.__selected_team.challengers = []
        self.__selected_team.unsuported_challengers = []

        self.__running = False

    def pop_challenger(self, number):
        if not self.__selected_team:
            print('No selected team !')
            return
        if len(self.__selected_team.challengers) == 0:
            print('No available challenger !')
            return
        
        if len(self.__selected_team.challengers)-1 < number:
            print('NO NEXT CHALLENGER')
            return

        self.__running = True

        if number == 0:
            x = -15
            y = -15.5
            rotation = 0
        elif number == 1:
            x = -16
            y = 23
            rotation = 2.354
        elif number == 2:
            x = -47
            y = 57
            rotation = 1.552
        else:
            return

        challenger = self.__selected_team.challengers[number]

        controller = ', controller "%s"' % (challenger.controller)

        settings = ''
        if challenger.robot_settings:
            print(challenger.robot_settings)
            for s in challenger.robot_settings:
                settings += ',' + s

        node_name = challenger.name

        # With 'DEF' we can set Node definition
        robot_def = 'DEF %s %s { \
            translation %s %s 2.1, \
            rotation 0 0 1 %s, \
            name "%s" %s %s }' \
            % (node_name, challenger.robot, x, y, rotation, challenger.name, controller, settings)

        from pprint import pprint
        pprint(robot_def)

        self.getRoot().getField('children').importMFNodeFromString(-1, robot_def)
        self.__selected_team.challengers[number].simu_DEF = self.getFromDef(
            node_name)
        
        return self.__selected_team.challengers[number].simu_DEF

