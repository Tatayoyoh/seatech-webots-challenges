from os.path import abspath, dirname, join, exists
from os import listdir, walk
from pprint import pprint
import random, math
from controller import Supervisor, Node, Robot
from webots_parser import WebotsParser
import pyjq

GENERIC_CONTROLLER_NAME = 'my_controller'
BATTLE_ROBOTS_NUMBER = 20

ROBOT_LIST = [
    'Fabtino',
    'SickS300',
    'TurtleBot3Burger',
    'RobotisLds01',
    'Astra',
    'Rosbot',
    'E-puck',
    'HokuyoUrg04lxug01',
    'SummitXlSteel',
    'Tiago++',
    'Robotino3',
]

ARENA_SIDE_SIZE = 3

SLOT_QUERY = '.root[0].fields[] | select(.name == $robotname).value.fields[] | select(.name | test(".*slot";"i"))'

class Challenger():
    name = None
    src_path = None
    robot = ''
    controller = ''
    world = None
    robot_settings = []

    def __init__(self, name, src_path):
        self.name = name
        self.src_path = src_path

    def __repr__(self) -> str:
        return '%s (%s): %s %s [%s]'%(self.name, self.src_path, self.robot, self.controller, self.robot_settings)

    def __str__(self) -> str:
        return self.__repr__()


class SeatechBattleSupervisor(Supervisor):
    def __init__(self):
        super().__init__()
        # 'challengers' folder is created by 'fetch_challengers_repositories.py' script
        self.__controllers_folder = abspath(join(dirname(abspath(__name__)), '..'))
        self.__challengers_folder = abspath(join(dirname(abspath(__name__)), '../../challengers'))
        self.__challengers = []
        self.__unsuported_challengers = []
        self.__running = False

        self.__root_children = self.getRoot().getField('children')

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
        # fetch folder
        for challenger_name in listdir(self.__challengers_folder):
            challenger = Challenger(name=challenger_name, src_path=join(self.__challengers_folder))
            for root, dirs, files in walk(challenger.src_path):
                if 'worlds' in dirs and 'controllers' in dirs:
                    controller_name = '%s_%s'%(GENERIC_CONTROLLER_NAME, challenger.name)
                    controller_path = join(self.__controllers_folder, controller_name)
                    challenger_world_file = join(root, 'worlds', 'simu.wbt')
                    if exists(controller_path) and exists(challenger_world_file):
                        proto = WebotsParser(verbose=False)
                        proto.load(challenger_world_file)
                        # get robot controller name
                        challenger.controller = controller_name
                        # get robot World
                        challenger.world = challenger_world_file
                        # get robot Name
                        challenger.robot = self.__get_used_robot(str(proto.content))
                        # get robot Slots
                        robot_slots = pyjq.all(SLOT_QUERY, proto.content, vars={'robotname':challenger.robot})
                        for slot in robot_slots:
                            proto.write_content = ''
                            proto._write_field(slot)
                            challenger.robot_settings.append(proto.write_content.replace('\n', ''))
                        self.__challengers.append(challenger)
                    else:
                        self.__unsuported_challengers.append(challenger)
                    break

    def __pop_robot(self, challenger:Challenger):
        x = random.uniform(-ARENA_SIDE_SIZE, ARENA_SIDE_SIZE)
        y = random.uniform(-ARENA_SIDE_SIZE, ARENA_SIDE_SIZE)
        rotation = random.uniform(-math.pi, math.pi)

        print(controller)
        print(x, y, rotation)

        if challenger.controller:
            controller = ', controller "%s"'%(controller)
        
        node_name = challenger.name

        # With 'DEF' we can set Node definition
        robot_def = 'DEF %s SummitXlSteel { \
            translation %s %s 2.1, \
            rotation 0 0 1 %s, \
            name "%s"' \
            %(node_name, challenger.robot, x, y, rotation, challenger.name, controller)
        
        self.__root_children.importMFNodeFromString(-1, robot_def)

        self.__robots[node_name] = self.getFromDef(node_name)

    def clear(self):
        for robot in self.__robots.values():
            robot.remove()
            del robot
        self.__robots.clear()

        for token in self.__tokens.values():
            token.remove()
            del token
        self.__tokens.clear()

        self.__running = False

                
    def pop_challengers(self):
        self.__running = True
        for challenger in self.__challengers:
            self.__pop_robot(challenger)
