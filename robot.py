import os

import magicbot
import wpilib
from ctre import WPI_TalonSRX
from navx import AHRS
from wpilib import SPI,Joystick

from components.chassis import Chassis
from jokerpylib.mapping.map import Map

"""
This is a template for magicbot project for FRC Team 4320 - The Jokerbot
"""


class Jokerbot(magicbot.MagicRobot):
    chassis: Chassis

    def createObjects(self):
        '''Create motors and stuff here'''

        with self.consumeExceptions():
            Map.load_json(os.path.join(os.path.dirname(os.path.realpath(__file__)),"map.json"))

        self.chassis_ports = Map.get_map()["subsystems"]["chassis"]["can_motors"]

        self.chassis_left_master = WPI_TalonSRX(self.chassis_ports["left_master"])
        self.chassis_left_slave = WPI_TalonSRX(self.chassis_ports["left_slave"])
        self.chassis_right_master = WPI_TalonSRX(self.chassis_ports["right_master"])
        self.chassis_right_slave = WPI_TalonSRX(self.chassis_ports["right_slave"])

        self.chassis_navx = AHRS.create_spi()

        self.left_joystick = Joystick(Map.get_map()["operator_ports"]["left_stick"])

    def teleopInit(self):
        '''Called when teleop starts; optional'''
        pass

    def teleopPeriodic(self):
        '''Called on each iteration of the control loop'''
        self.chassis.upadte_operator(self.left_joystick)


if __name__ == "__main__":
    wpilib.run(Jokerbot)
