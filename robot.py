import magicbot
import wpilib
from components import my_component
from wpilib import Talon

"""
This is a template for magicbot project for FRC Team 4320 - The Jokerbot
"""

class Jokerbot(magicbot.MagicRobot):

    my_component: my_component.MyComponent

    def createObjects(self):
        '''Create motors and stuff here'''
        self.my_component_motor = Talon(0)


    def teleopInit(self):
        '''Called when teleop starts; optional'''
        pass

    def teleopPeriodic(self):
        '''Called on each iteration of the control loop'''
        pass

if __name__ == "__main__":
    wpilib.run(Jokerbot)