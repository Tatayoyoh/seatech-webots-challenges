from webots_parser import WebotsParser
import pyjq
from pprint import pprint
from os.path import abspath, dirname, join, exists
from os import listdir, walk
from seatech_battle_supervisor import ROBOT_LIST, SLOT_QUERY, GENERIC_CONTROLLER_NAME
from seatech_battle_supervisor import Challenger, SeatechBattleSupervisor

files = [
    '/home/bob/Projects/seatech/seatech-webots-challenges/2023-super-smash-bot-melee/challengers/RCLEMENT404/webot/worlds/simu.wbt',
    '/home/bob/Projects/seatech/seatech-webots-challenges/2023-super-smash-bot-melee/challengers/mlola378/webots/worlds/simu.wbt',
    '/home/bob/Projects/seatech/seatech-webots-challenges/2023-super-smash-bot-melee/challengers/Jacint012/webots/worlds/simu.wbt',
    '/home/bob/Projects/seatech/seatech-webots-challenges/2023-super-smash-bot-melee/challengers/IUT-Bares-Coline/Webots/worlds/simu.wbt',
    '/home/bob/Projects/seatech/seatech-webots-challenges/2023-super-smash-bot-melee/challengers/ClaireGyt/simu-2023/worlds/simu.wbt',
    '/home/bob/Projects/seatech/seatech-webots-challenges/2023-super-smash-bot-melee/challengers/TeTan0s/Webot/worlds/simu.wbt',
    '/home/bob/Projects/seatech/seatech-webots-challenges/2023-super-smash-bot-melee/challengers/Lucaslh83/02-webots/worlds/simu.wbt'
]

SLOT_QUERY = '.root[-1].fields[] | select(.name == $robotname).value.fields[] | select(.name | test(".*slot";"i"))'
SLOT_QUERY = '.root[].fields[] | select(.name | test(".*slot";"i"))'



# def get_used_robot(proto_content):
#     for r in ROBOT_LIST:
#         if r in proto_content:
#             return r
#     return None

# for f in files :
#     proto = WebotsParser(verbose=False)
#     proto.load(f)

#     challenger_robot = get_used_robot(proto.content)

#     print(challenger_robot)

#     robot_slots = pyjq.all(SLOT_QUERY, proto.content)

#     # pprint(robot_slots)

#     for slot in robot_slots:
#         proto.write_content = ''
#         proto._write_field(slot)
#         # print(proto.write_content.replace('\n', ''))

#     pprint(robot_slots)


# class SeatechBattleSupervisor():
#     def __init__(self):
#         # 'challengers' folder is created by 'fetch_challengers_repositories.py' script
#         self.__controllers_folder = abspath(join(dirname(abspath(__name__)), '..'))
#         self.__challengers_folder = abspath(join(dirname(abspath(__name__)), '../../challengers'))
#         self.__challengers = []
#         self.__unsuported_challengers = []

#         self.__fetch_challengers_robots()

#     def __get_used_robot(self, proto_content):
#         for r in ROBOT_LIST:
#             if r in proto_content:
#                 return r
#         return None

#     def __fetch_challengers_robots(self):
#         self.__challengers = []
#         self.__unsuported_challengers = []

#         # fetch folder
#         for challenger_name in listdir(self.__challengers_folder):
#             challenger = Challenger(
#                 name=challenger_name, 
#                 src_path=join(self.__challengers_folder, challenger_name)
#             )
#             print('CHALLENGER',challenger_name)
#             for root, dirs, files in walk(challenger.src_path):
#                 if 'worlds' in dirs and 'controllers' in dirs:
#                     controller_name = '%s_%s'%(GENERIC_CONTROLLER_NAME, challenger.name)
#                     controller_path = join(self.__controllers_folder, controller_name)
#                     challenger_world_file = join(root, 'worlds', 'simu.wbt')
#                     if exists(controller_path) and exists(challenger_world_file):
#                         print(challenger_world_file)
#                         # parse Webots PROTO file
#                         proto = WebotsParser(verbose=False)
#                         proto.content = {}
#                         proto.load(challenger_world_file)
#                         # pprint(proto.content)
#                         # get robot controller name
#                         challenger.controller = controller_name
#                         # get robot World
#                         challenger.world = challenger_world_file
#                         # get robot Name
#                         challenger.robot = self.__get_used_robot(str(proto.content))
#                         # get robot Slots
#                         # robot_slots = pyjq.all(SLOT_QUERY, proto.content, vars={'robotname':challenger.robot})
#                         robot_slots = pyjq.all(SLOT_QUERY, proto.content)
#                         # print(challenger_world_file)
#                         # print(proto.content)
#                         print(robot_slots)
#                         for slot in robot_slots:
#                             print(proto.write_content)
#                             proto.write_content = ''
#                             proto._write_field(slot)
#                             challenger.robot_settings.append(proto.write_content.replace('\n', ''))
#                             print( )
#                             print(proto.write_content)
#                         # print(challenger.robot_settings)
#                         break

#             if challenger.robot and challenger.controller:
#                 self.__challengers.append(challenger)
#             else:
#                 self.__unsuported_challengers.append(challenger)


supervisor = SeatechBattleSupervisor(test_mode=True)