from time import time
from controller import Robot, DistanceSensor
from EpuckMotors import EpuckMotors
from EpuckCamera import EpuckCamera
from EpuckDistanceSensors import EpuckDistanceSensors


class SeatechEpuckRobot(Robot):

    def __init__(self, timestep=None, camera_sampling_period=1):
        super().__init__()
        
        # Engines
        self.__motors = EpuckMotors()
        self.__speed = self.__motors.get_max_speed()
        # Sensors
        self.__camera = EpuckCamera()
        self.__distance_sensors = EpuckDistanceSensors()

        # Internal datas
        self.__goal_name = None
        self.__goal_reached = False
        self.__timestep = timestep
        self.__camera_sampling_period = camera_sampling_period

    @property
    def goal_reached(self):
        return self.__goal_reached

    def track_object(self, object_name):
        self.__goal_name = object_name
        self.__camera.track_object(object_name)

    def __process_recognition(self):

        if self.__camera.is_tracked_object_on_left():
            self.__turn_left(capacity=0.5)
        if self.__camera.is_tracked_object_on_right():
            self.__turn_right(capacity=0.5)
        # if self.__camera.is_tracked_object_present():
        #     self.__goal_reached = True

    def __turn_left(self, capacity=0.6):
        self.__motors.turn_left(capacity=capacity)

    def __turn_right(self, capacity=0.6):
        self.__motors.turn_right(capacity=capacity)
    
    def __run(self):
        self.__motors.run(speed=self.__speed)

        # process recognition every X steps
        if round(self.getTime() % self.__camera_sampling_period , 1) == 0.1:
            self.__process_recognition()

        if self.__distance_sensors.front_right_collision_detected():
            self.__turn_left()
        elif self.__distance_sensors.front_left_collision_detected():
            self.__turn_right()

    def stop(self):
        self.__motors.run(speed=0)

    def start_mission(self):
        # Check goal is ok
        if not isinstance(self.__goal_name, str):
            print('ERROR: goal to reach is not a string name : %s', self.__goal_name)
            return False

        # Run mission
        while self.step(self.__timestep) != -1:
            self.__run()
            if self.goal_reached:
                print('VICTORY !! Found', self.__goal_name)
                break

        # Stop the robot when mission is done
        self.stop()
