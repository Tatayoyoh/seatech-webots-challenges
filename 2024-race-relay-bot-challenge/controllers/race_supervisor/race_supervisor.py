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

    # First challenger
    challenger1 = supervisor.pop_challenger(0)
    challenger2 = None
    challenger3 = None

    while supervisor.step(supervisor.timestep) != -1:
        key = keyboard.getKey()
        key = chr(key).upper() if key != -1 else None
        
        if challenger1:
            ch1_pos = challenger1.getPosition()
            if ch1_pos[0] > -19 and ch1_pos[0] < -13 and ch1_pos[1] > 20 and ch1_pos[1] < 26:
                challenger1.remove()
                challenger1 = None
                challenger2 = supervisor.pop_challenger(1)
        elif challenger2:
            ch2_pos = challenger2.getPosition()
            if ch2_pos[0] > -46 and ch2_pos[0] < -40 and ch2_pos[1] > 48 and ch2_pos[1] < 53:
                challenger2.remove()
                challenger2 = None
                challenger3 = supervisor.pop_challenger(2)

        if key == 'Q':
            break
        elif key == 'R':
            supervisor.clear()
            challenger1 = supervisor.pop_challenger(0)
            challenger2 = None
            challenger3 = None
            print('>>> SIMU RESETED')



    print('Bye !')