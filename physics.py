#
# See the notes for the other physics sample
#
import math
from pyfrc.physics import motor_cfgs, tankmodel
from pyfrc.physics.units import units

from jokerpylib.mapping.map import Map


class PhysicsEngine(object):
    """
       Simulates a 4-wheel robot using Tank Drive joystick control
    """

    def __init__(self, physics_controller):
        """
            :param physics_controller: `pyfrc.physics.core.Physics` object
                                       to communicate simulation effects to
        """

        self.physics_controller = physics_controller
        self.physics_controller.add_device_gyro_channel("navxmxp_spi_4_angle")

        # Change these parameters to fit your robot!
        bumper_width = 3.25 * units.inch

        # fmt: off
        self.drivetrain = tankmodel.TankModel.theory(
            motor_cfgs.MOTOR_CFG_CIM,  # motor configuration
            110 * units.lbs,  # robot mass
            10.71,  # drivetrain gear ratio
            2,  # motors per side
            22 * units.inch,  # robot wheelbase
            23 * units.inch + bumper_width * 2,  # robot width
            32 * units.inch + bumper_width * 2,  # robot length
            6 * units.inch,  # wheel diameter
        )
        # fmt: on

    def update_sim(self, hal_data, now, tm_diff):
        """
            Called when the simulation parameters for the program need to be
            updated.

            :param now: The current time as a float
            :param tm_diff: The amount of time that has passed since the last
                            time that this function was called
        """

        """For drivetrain simulation"""
        # Not needed because front and rear should be in sync
        lm_motor = hal_data['CAN'][0]['value']
        rm_motor = hal_data['CAN'][1]['value']

        x, y, angle = self.drivetrain.get_distance(lm_motor, rm_motor, tm_diff)
        self.physics_controller.distance_drive(x, y, angle)

        constants = Map.get_map()["subsystems"]["chassis"]["constants"]

        encoder_ratio = constants["encoder_ratio"]
        wheel_diam = constants["wheel_diam"]
        high_gear_ratio = constants["high_gear_ratio"]
        encoder_ticks = constants["encoder_ticks"]

        wheel_circumference = wheel_diam * math.pi

        ticks_per_rev = high_gear_ratio * encoder_ratio * encoder_ticks
        ticks_per_feet = ticks_per_rev * wheel_circumference

        hal_data['CAN'][0]['quad_position'] = self.drivetrain.l_position * ticks_per_feet
        hal_data['CAN'][1]['quad_position'] = self.drivetrain.r_position * ticks_per_feet

        # TODO convert velocity measurement units
        hal_data['CAN'][0]['quad_velocity'] = self.drivetrain.l_velocity
        hal_data['CAN'][1]['quad_velocity'] = self.drivetrain.r_velocity
