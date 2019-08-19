import os

from magicbot import AutonomousStateMachine

# this is one of your components
from components.chassis import Chassis
from jokerpylib.mapping.map import Map
from jokerpylib.pathing.path_follower import PathFollower


class MotionProfileStateMachine(AutonomousStateMachine):
    chassis: Chassis
    def __init__(self):
        super().__init__()
        self.path_follower: PathFollower = None

    def create_path_follower(self, name, kp, ki, kd, reverse=False):
        leftn = Map.get_map()["paths"][name]["left"]
        rightn = Map.get_map()["paths"][name]["right"]
        dir = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))

        leftn = os.path.join(dir, leftn)
        rightn = os.path.join(dir, rightn)
        constants = Map.get_map()["subsystems"]["chassis"]["constants"]

        encoder_ratio = constants["encoder_ratio"]
        third_stage_ratio = constants["third_stage_ratio"]
        encoder_ticks = constants["encoder_ticks"]
        wheel_diam = constants["wheel_diam"]

        ticks_per_rev = third_stage_ratio * encoder_ratio * encoder_ticks

        kv = 1.0 / 21.0
        ka = 0

        left_offset, right_offset = self.chassis.get_encoder_ticks()
        self.path_follower = PathFollower(leftn, rightn, ticks_per_rev, wheel_diam, [kp, ki, kd, kv, ka],
                                          self.chassis.set_motors_values, self.chassis.get_encoder_ticks,
                                          self.chassis.get_angle, reverse, left_offset, right_offset)
