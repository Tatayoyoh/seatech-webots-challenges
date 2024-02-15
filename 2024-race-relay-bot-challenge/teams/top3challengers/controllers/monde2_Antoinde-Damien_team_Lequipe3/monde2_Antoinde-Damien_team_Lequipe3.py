"""my_controller controller."""

# You may need to import some classes of the controller module. Ex:
#  from controller import Robot, Motor, DistanceSensor
from controller import Robot ,Motor , DistanceSensor, Compass
import math

class Motors ():

    def __init__(self,robot:Robot):
        super().__init__()
        self.lwheel : Motor = robot.getDevice('left wheel')
        self.rwheel : Motor = robot.getDevice('right wheel')
        self.lwheel.setPosition(float("inf"))
        self.rwheel.setPosition(float("inf"))

    def turn_left(self, Value):
        self.lwheel.setVelocity(-Value)
        self.rwheel.setVelocity(Value)

    def turn_right(self, Value):
        self.lwheel.setVelocity(Value)
        self.rwheel.setVelocity(-Value)

    def forward(self, Value):
        self.lwheel.setVelocity(Value)
        self.rwheel.setVelocity(Value)

    def backward(self, Value):
        self.lwheel.setVelocity(-Value)
        self.rwheel.setVelocity(-Value)

class monRobot(Robot):
    
    def __init__(self):
        super().__init__()
    
        self.timestep = int(self.getBasicTimeStep())
        self.motors=Motors(self)

        self.so1:DistanceSensor = self.getDevice('so1')
        self.so2:DistanceSensor = self.getDevice('so2')
        self.so3:DistanceSensor = self.getDevice('so3')
        self.so4:DistanceSensor = self.getDevice('so4')
        self.so5:DistanceSensor = self.getDevice('so5')
        self.so6:DistanceSensor = self.getDevice('so6')

        self.so1.enable(self.timestep)
        self.so2.enable(self.timestep)
        self.so3.enable(self.timestep)
        self.so4.enable(self.timestep)
        self.so5.enable(self.timestep)
        self.so6.enable(self.timestep)
        self.compass:Compass = self.getDevice('compass')
        self.compass.enable(self.timestep)

        self.route = False
        self.test_cap = 0

    def cap(self, cap_actuel, cap_vise):


        if ( cap_vise - 1 > cap_actuel)  or  (cap_actuel > cap_vise + 1):

            if  cap_actuel >= cap_vise:
                
                self.motors.turn_left(1)
                cap_actuel = self.ValueCompass()
            elif cap_actuel <= cap_vise:
                
                self.motors.turn_right(1)
                cap_actuel = self.ValueCompass()

        else: 
            self.route = True

    def run(self):
        
        
        print("so1 : ",self.so1.getValue())
        print("so2 : ",self.so2.getValue())
        print("so3 : ",self.so3.getValue())
        print("s04 : ",self.so4.getValue())
        print("s05 : ",self.so5.getValue())
        print("s06 : ",self.so6.getValue())
        
        
        if self.route == False :
            self.cap(self.ValueCompass() , 225)

        elif self.so1.getValue() >= 950 or self.so2.getValue() >= 950 or self.so3.getValue() >= 950:
              
            self.motors.turn_right(5)
           
        elif self.so6.getValue() >= 950 or self.so5.getValue() >= 950 or self.so4.getValue() >= 950:

            self.motors.turn_left(5)

        elif self.test_cap == 40:

            self.test_cap = 0
            self.route = False

        else:
            self.motors.forward(9)
            self.test_cap +=1
        pass
        
        print(self.ValueCompass())

    def ValueCompass(self):
        north = self.compass.getValues()
        rad = math.atan2(north[1], north[0])
        bearing = (rad - 1.5708) / math.pi * 180.0
        if (bearing < 0.0):
            bearing = bearing + 360.0
        return bearing



# create the Robot instance.
robot = monRobot()

# get the time step of the current world.


# You should insert a getDevice-like function in order to get the
# instance of a device of the robot. Something like:
#  motor = robot.getDevice('motorname')
#  ds = robot.getDevice('dsname')
#  ds.enable(timestep)

# Main loop:
# - perform simulation steps until Webots is stopping the controller
while robot.step(robot.timestep) != -1:

    robot.run() # on avance et on esquive les murs



    # Read the sensors:
    # Enter here functions to read sensor data, like:
    #  val = ds.getValue()

    # Process sensor data here.

    # Enter here functions to send actuator commands, like:
    #  motor.setPosition(10.0)
    pass

# Enter here exit cleanup code.
