from seatech_battle_supervisor import  SeatechBattleSupervisor


if __name__ == '__main__':

    supervisor = SeatechBattleSupervisor(test_mode=True)


    print('CHALLENGERS:')
    for c in supervisor.challengers:
        print(c.name, c.robot)

    print()
    if supervisor.unsuported_challengers:
        print('UNSUPORTED CHALLENGERS:')
        for c in supervisor.unsuported_challengers:
            print(c.name, c.robot)
