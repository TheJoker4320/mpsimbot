import magicbot
import wpilib
from components.chassis import Chassis
from wpilib import Talon
from ctre import WPI_TalonSRX

"""
This is a template for magicbot project for FRC Team 4320 - The Jokerbot
"""

class Jokerbot(magicbot.MagicRobot):

    chassis: Chassis

    def createObjects(self):
        '''Create motors and stuff here'''
        self.chassis_left_master = WPI_TalonSRX()
        self.chassis_left_slave = WPI_TalonSRX()
        self.chassis_right_master = WPI_TalonSRX()
        self.chassis_right_slave = WPI_TalonSRX()


    def teleopInit(self):
        '''Called when teleop starts; optional'''
        pass

    def teleopPeriodic(self):
        '''Called on each iteration of the control loop'''
        pass

if __name__ == "__main__":
    wpilib.run(Jokerbot)