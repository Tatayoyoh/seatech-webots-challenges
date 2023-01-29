from controller import Keyboard
from seatech_battle_supervisor import SeatechBattleSupervisor


if __name__ == '__main__':

    supervisor = SeatechBattleSupervisor()
    time_step = int(supervisor.getBasicTimeStep())
    # supervisor.pop_challengers()

    keyboard = Keyboard(time_step)
    # keyboard.enable(KEYBOARD_SAMPLING_PERIOD)
    print('Student folder:', supervisor.challengers_folder)

    print('CHALLENGERS:')
    for c in supervisor.challengers:
        print(c.name, c.robot)

    if supervisor.unsuported_challengers:
        print('UNSUPORTED CHALLENGERS:')
        for c in supervisor.unsuported_challengers:
            print(c.name, c.robot)


    while supervisor.step(time_step) != -1:        
        # if supervisor.running:
        key = keyboard.getKey()
        key = chr(key).upper() if key != -1 else None
        if key == 'R':
            supervisor.clear()
            print('Removed all challengers !')
        elif key == 'Q':
            break

    print('Bye !')