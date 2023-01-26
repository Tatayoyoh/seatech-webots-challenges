from SeatechEpuckRobot import SeatechEpuckRobot

if __name__ == '__main__':
    TIME_STEP = 64

    # create the Robot instance.
    robot = SeatechEpuckRobot(TIME_STEP)
    robot.track_object('rubber duck')
    robot.start_mission()

