from os.path import abspath, dirname, join, exists
from os import listdir, walk
from pprint import pprint
import random, math
from controller import Supervisor
from webots_parser import WebotsParser
import pyjq

GENERIC_CONTROLLER_NAME = 'my_controller'
BATTLE_ROBOTS_NUMBER = 20

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
]

ARENA_SIDE_SIZE = 3

# SLOT_QUERY = '.root[0].fields[] | select(.name == $robotname).value.fields[] | select(.name | test(".*slot";"i"))'
SLOT_QUERY = '.root[].fields[] | select(.name | test(".*slot";"i"))'

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
        return '%s (%s): %s %s [%s]'%(self.name, self.src_path, self.robot, self.controller, self.robot_settings)

    def __str__(self) -> str:
        return self.__repr__()


class SeatechBattleSupervisor(Supervisor):
    def __init__(self, test_mode=False):
        if not test_mode:
            super().__init__()
        # 'challengers' folder is created by 'fetch_challengers_repositories.py' script
        self.__controllers_folder = abspath(join(dirname(abspath(__name__)), '..'))
        self.__challengers_folder = abspath(join(dirname(abspath(__name__)), '../../challengers'))
        self.__challengers = []
        self.__unsuported_challengers = []
        self.__running = False

        self.__fetch_challengers_robots()

    @property
    def challengers(self):
        return self.__challengers

    @property
    def unsuported_challengers(self):
        return self.__unsuported_challengers

    @property
    def challengers_folder(self):
        return self.__challengers_folder

    @property
    def running(self):
        return self.__running

    def __get_used_robot(self, proto_content):
        for r in ROBOT_LIST:
            if r in proto_content:
                return r
        return None

    def __fetch_challengers_robots(self):
        self.__challengers = []
        self.__unsuported_challengers = []

        # fetch folder
        for challenger_name in listdir(self.__challengers_folder):
            challenger = Challenger(
                name=challenger_name, 
                src_path=join(self.__challengers_folder, challenger_name)
            )
            for root, dirs, files in walk(challenger.src_path):
                if 'worlds' in dirs and 'controllers' in dirs:
                    controller_name = '%s_%s'%(GENERIC_CONTROLLER_NAME, challenger.name)
                    controller_path = join(self.__controllers_folder, controller_name)
                    challenger_world_file = join(root, 'worlds', 'simu.wbt')
                    if exists(controller_path) and exists(challenger_world_file):
                        # parse Webots PROTO file
                        proto = WebotsParser(verbose=False)
                        proto.load(challenger_world_file)
                        # get robot controller name
                        challenger.controller = controller_name
                        # get robot World
                        challenger.world = challenger_world_file
                        # get robot Name
                        challenger.robot = self.__get_used_robot(str(proto.content))
                        # get robot Slots
                        robot_slots = pyjq.all(SLOT_QUERY, proto.content)

                        for slot in robot_slots:
                            proto.write_content = ''
                            proto._write_field(slot)
                            challenger.robot_settings.append(proto.write_content.replace('\n', ''))

                        break

            if challenger.robot and challenger.controller:
                self.__challengers.append(challenger)
            else:
                self.__unsuported_challengers.append(challenger)

    def clear(self):
        for challenger in self.challengers:
            challenger.simu_DEF.remove()
            challenger.simu_DEF = None

        self.__challengers = []
        self.__unsuported_challengers = []   

        self.__running = False

                
    def pop_challengers(self):
        self.__running = True
        for i, challenger in enumerate(self.__challengers):
            x = random.uniform(-ARENA_SIDE_SIZE, ARENA_SIDE_SIZE)
            y = random.uniform(-ARENA_SIDE_SIZE, ARENA_SIDE_SIZE)
            rotation = random.uniform(-math.pi, math.pi)
            # TODO : not twice same place

            controller = ', controller "%s"'%(challenger.controller)
            
            settings = ''
            if challenger.robot_settings:
                for s in challenger.robot_settings:
                    settings += ',' + s

            node_name = challenger.name

            # With 'DEF' we can set Node definition
            robot_def = 'DEF %s %s { \
                translation %s %s 2.1, \
                rotation 0 0 1 %s, \
                name "%s" %s %s }' \
                %(node_name, challenger.robot, x, y, rotation, challenger.name, controller, settings)

            self.getRoot().getField('children').importMFNodeFromString(-1, robot_def)
            self.challengers[i].simu_DEF = self.getFromDef(node_name)
