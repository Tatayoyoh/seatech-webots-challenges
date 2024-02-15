from webots_parser import WebotsParser
import pyjq
from pprint import pprint
from os.path import abspath, dirname, join, exists
from os import listdir, walk
from seatech_battle_supervisor import ROBOT_LIST, SLOT_QUERY, GENERIC_CONTROLLER_NAME
from seatech_battle_supervisor import Challenger, SeatechBattleSupervisor, jq

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

#     robot_slots = jq(SLOT_QUERY, proto.content)

#     # pprint(robot_slots)

#     for slot in robot_slots:
#         proto.write_content = ''
#         proto._write_field(slot)
#         # print(proto.write_content.replace('\n', ''))

#     pprint(robot_slots)



supervisor = SeatechBattleSupervisor(test_mode=True)


print('CHALLENGERS:')
for c in supervisor.challengers:
    print(c.name, c.robot)

print()
if supervisor.unsuported_challengers:
    print('UNSUPORTED CHALLENGERS:')
    for c in supervisor.unsuported_challengers:
        print(c.name, c.robot)
