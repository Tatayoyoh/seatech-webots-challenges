from os.path import abspath, dirname, join, exists
from os import listdir, walk
from pprint import pprint
from controller import Supervisor
from webots_parser import WebotsParser
import shutil
import pathlib
from pprint import pprint
import os
import json

# SLOT_QUERY = '.root[0].fields[] | select(.name == $robotname).value.fields[] | select(.name | test(".*slot";"i"))'

def jq(jq_expression, data, as_list=False):
    """ call jq command """
    cmd = "echo '%s' | jq '%s'"%(json.dumps(data), jq_expression)
    res = os.popen(cmd).read()
    if res:
        res = json.loads(res)
        if as_list and type(res) != list:
            res = [res]
    else:
        if as_list:
            res = []
    return res

class Team():
    def __init__(self, name, repo_path):
        self.name: str = name
        self.repo_path = repo_path
        self.world_file = ''
        self.challengers: list[Challenger] = []
        self.unsuported_challengers: list[Challenger] = []

    def __repr__(self) -> str:
        return "%s"%(self.name)

    def __str__(self) -> str:
        return self.__repr__()

class Challenger():

    def __init__(self, name, src_path):
        self.name = name
        self.src_path = src_path
        self.robot = ''
        self.world_proto = {}
        self.controller = ''
        self.world = None
        self.slots = []
        self.simu_DEF = None

    def slots_to_proto(self):
        parser = WebotsParser()
        proto_slots = []

        for slot in self.slots:
            with open('/tmp/slots', 'w', newline='\n') as parser.file:
                parser._write_field(slot)
            with open('/tmp/slots', 'r') as parser.file:
                proto_content = parser.file.read()
                proto_slots.append(proto_content.replace('\n', ''))
    
        if proto_slots:
            return ', '+ ','.join(proto_slots)
        
        return ''

    def __repr__(self) -> str:
        return '%s (%s): %s %s [%s]' % (self.name, self.src_path, self.robot, self.controller, self.slots_to_proto())

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

    def __fetch_teams(self):
        for team_name in listdir(self.__teams_folder):
            team = Team(team_name, repo_path=join(self.__teams_folder, team_name))
            for root, dirs, files in walk(team.repo_path):
                if 'worlds' in dirs and 'controllers' in dirs:
                    world_path = join(team.repo_path, 'worlds')
                    worlds = list(pathlib.Path(world_path).glob('*.wbt'))
                    if len(worlds) > 0:
                        team.world_file = worlds[0]
                    else:
                        raise Exception('No world .wbt found for team %s at %s'%(team.name, world_path))
            self.__teams.append(team) 

    def select_team(self, index):
        if len(self.__teams) < index or index < 0:
            print("Wrong provided team index : %s. Total teams : %d"%index, len(self.__teams))
            return
        
        self.__selected_team = self.__teams[index]
        team:Team = self.__selected_team

        team.challengers = []
        team.unsuported_challengers = []

        # fetch Team challengers and controllers
        controllers = list(listdir(join(team.repo_path, 'controllers')))
        controllers.sort()
        for controller_name in controllers:
            print('-----------------')
            print(controller_name)
            controller_path = join(team.repo_path, 'controllers', controller_name)

            challenger = Challenger(
                name=controller_name,
                src_path=controller_path
            )

            if exists(controller_path) and exists(team.world_file):
                # get robot controller name
                challenger.controller = team.name+'_'+controller_name

                # parse Webots PROTO file
                try:
                    proto = WebotsParser()
                    proto.load(team.world_file)

                    # copy controller into simulation "controllers" folder
                    controller_copy = join(self.__controllers_folder, challenger.controller)
                    if exists(controller_copy):
                        shutil.rmtree(controller_copy)
                    shutil.copytree(controller_path, controller_copy)
                    shutil.move(join(controller_copy,controller_name+'.py'), join(controller_copy,challenger.controller+'.py'))
                except Exception as e:
                    print('ERROR', str(challenger))
                    print(e)
                    continue

                CONTROLLER_QUERY = '.root[] | select(.fields[].value == "%s")'%(controller_name)
                ROBOT_NAME_QUERY = '.root[] | select(.fields[].value == "%s") | .name'%(controller_name)
                SLOT_QUERY = '.root[] | select(.fields[].value == "%s") | .fields[] | select(.name | test(".*slot";"i"))'%(controller_name)

                # get robot Proto
                challenger.world_proto = jq(CONTROLLER_QUERY, proto.content)
                print(challenger.world_proto)
                # get robot Name
                challenger.robot = jq(ROBOT_NAME_QUERY, proto.content)
                print(challenger.robot)
                # get robot Slots
                challenger.slots = jq(SLOT_QUERY, proto.content, as_list=True)
                print(challenger.slots)

                
                print("Challenger %s. Found slots : {%s}"%(challenger.controller, challenger.slots_to_proto()))

                if challenger.robot and challenger.controller:
                    team.challengers.append(challenger)
                else:
                    team.unsuported_challengers.append(challenger)
            else:
                raise Exception('Missing "worlds" or "controllers" path for team %s'%(team.name))
        
        print('IMPORTED', len(team.challengers))
        print('IGNORED', team.unsuported_challengers)

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
            z = 0.1
            rotation = 0
        elif number == 1:
            x = -16
            y = 23
            z = 0.03
            rotation = 2.354
        elif number == 2:
            x = -47
            y = 57
            z = 0.1
            rotation = 1.552
        else:
            return

        challenger = self.__selected_team.challengers[number]

        controller = ', controller "%s"' % (challenger.controller)

        node_name = challenger.name

        # With 'DEF' we can set Node definition
        robot_def = 'DEF %s %s { \
            translation %s %s %s, \
            rotation 0 0 1 %s, \
            name "%s" %s %s }' \
            % (node_name, challenger.robot, x, y, z, rotation, challenger.name, controller, challenger.slots_to_proto())


        self.getRoot().getField('children').importMFNodeFromString(-1, robot_def)
        self.__selected_team.challengers[number].simu_DEF = self.getFromDef(
            node_name)
        
        print('SELECTED %s:'%(number))
        pprint(self.__selected_team.challengers[number])
        # print(robot_def)

        return self.__selected_team.challengers[number].simu_DEF

