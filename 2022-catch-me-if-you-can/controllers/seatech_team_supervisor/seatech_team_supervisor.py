from controller import Keyboard
from SeatechSupervisor import SeatechSupervisor

KEYBOARD_SAMPLING_PERIOD = 200
TIME_STEP = 64

def help_text():
    print('Which mode do you want to play ?')
    print('[A] Single random controller')
    print('[B] All controllers')
    print('[R] Reset')
    print('[Q] Quit')
    print('Enter your choice :')

if __name__ == '__main__':
    supervisor = SeatechSupervisor()

    keyboard = Keyboard()
    keyboard.enable(KEYBOARD_SAMPLING_PERIOD)

    print('Student folder:', supervisor.students_folder)
    help_text()

    choice = None

    while supervisor.step(TIME_STEP) != -1:        
        key = keyboard.getKey()
        
        if key != -1:
            key = chr(key).upper()

        if not supervisor.running:
            if key == 'A' :
                supervisor.set_single_random_controller_mode()
                print('Mode "Single random controller" activation')
            elif key == 'B':
                supervisor.set_all_controllers_mode()
                print('Mode "All controller" activation')

        if key == 'R':
            supervisor.clear()
            print('Removed all nodes !')
            help_text()
        
        if key == 'Q':
            print('Bye !')
            break

        if supervisor.running:
            supervisor.check_catcher_collisions()
            supervisor.update_token_positions()

