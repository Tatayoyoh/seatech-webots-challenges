from controller import Keyboard
from seatech_race_supervisor import SeatechRaceSupervisor


if __name__ == '__main__':
    start_ready = False
    supervisor = SeatechRaceSupervisor()
    keyboard = Keyboard(supervisor.timestep)

    print('Available Teams :')
    teams_letters = ['A','B','C','D'] # my Linux keybords not not accept numbers from Webots :(
    
    for i, team in enumerate(supervisor.teams):
        print(teams_letters[i], team)

    chose = input()
    team_number = teams_letters.index(chose)
    supervisor.select_team(team_number)
    supervisor.fetch_challengers_robots()
    print('>>> READY TO START WITH %s'%(supervisor.teams[team_number]))

    supervisor.pop_challenger(0)
    while supervisor.step(supervisor.timestep) != -1:
        key = keyboard.getKey()
        key = chr(key).upper() if key != -1 else None
        
        if key == 'S':
            pass
        # if key == 'R':
        #     supervisor.clear()
        #     supervisor.pop_challenger(1)
        #     print('>>> SIMU RESETED')
        elif key == 'Q':
            break

        if supervisor.running:
            pass
            # TODO pop first

            # TODO monitor first position
        
            # TODO pop second
        
            # TODO monitor second position

    # supervisor.pop_challenger(1)

    # if supervisor.unsuported_challengers:
    #     print('UNSUPORTED CHALLENGERS:')
    #     for c in supervisor.unsuported_challengers:
    #         print(c.name, c.robot)



    print('Bye !')