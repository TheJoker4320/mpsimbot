import os

from magicbot import AutonomousStateMachine, state, tunable

# this is one of your components
from components.chassis import Chassis
from jokerpylib.mapping.map import Map
from jokerpylib.pathing.path_follower import PathFollower


class StaightMP(AutonomousStateMachine):
    MODE_NAME = "3 meters mp"
    DEFAULT = False

    chassis: Chassis

    def setup(self):
        leftn = Map.get_map()["paths"]["circle"]["left"]
        rightn = Map.get_map()["paths"]["circle"]["right"]
        dir = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))

        leftn = os.path.join(dir, leftn)
        rightn = os.path.join(dir, rightn)
        constants = Map.get_map()["subsystems"]["chassis"]["constants"]

        encoder_ratio = constants["encoder_ratio"]
        third_stage_ratio = constants["third_stage_ratio"]
        encoder_ticks = constants["encoder_ticks"]
        wheel_diam = constants["wheel_diam"]

        ticks_per_rev = third_stage_ratio * encoder_ratio * encoder_ticks
        kp = 0.02
        ki = 0
        kd = 0
        kv = 1.0 / 21.0
        ka = 0

        left_offset, right_offset = self.chassis.get_encoder_ticks()
        self.path_follower = PathFollower(leftn, rightn, ticks_per_rev, wheel_diam, [kp, ki, kd, kv, ka],
                                          self.chassis.set_motors_values, self.chassis.get_encoder_ticks,
                                          self.chassis.get_angle, left_offset, right_offset)

    @state(first=True)
    def execute_path(self, initial_call):
        if initial_call:
            self.path_follower.start_following()

        if self.path_follower.is_finished():
            print("finished")
            super().done()
