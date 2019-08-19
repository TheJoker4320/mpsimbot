import pathfinder
from pathfinder.followers import EncoderFollower
from wpilib.notifier import Notifier


class PathFollower:

    def __init__(self, left_trajectory: str, right_trajectory: str, ticks_per_rev: int, wheel_diam: int, pidva: tuple,
                 setter, get_enc, get_angle, reverse=False,
                 left_offset: int = 0, right_offset: int = 0):

        self.setter = setter
        self.get_angle = get_angle
        self.get_enc = get_enc
        self.l_output = 0
        self.r_output = 0
        self.finished = False
        self.reverse = reverse
        self.notifier = Notifier(self._path_iteration)

        """
        Notice! Sides are intentionally flipped due to a bug on PathWeaver in 2019.
        If you use another software or manually create paths, uncomment the following lines,
        and comment out the lines for flipping paths
        """
        # self.left_traectory = pathfinder.deserialize_csv(left_trajectory)
        # self.right_trajectory = pathfinder.deserialize_csv(right_trajectory)

        # TODO fix this after pathweaver bug fix in 2020
        self.right_trajectory = pathfinder.deserialize_csv(left_trajectory)
        self.left_trajectory = pathfinder.deserialize_csv(right_trajectory)

        if self.reverse:
            temp_right = self.right_trajectory
            self.right_trajectory = self.left_trajectory
            self.left_trajectory = temp_right

        self.left_follower = EncoderFollower(self.left_trajectory)
        self.right_follower = EncoderFollower(self.right_trajectory)

        self.left_follower.configureEncoder(int(left_offset), int(ticks_per_rev), int(wheel_diam))
        self.right_follower.configureEncoder(int(right_offset), int(ticks_per_rev), int(wheel_diam))

        kp, ki, kd, kv, ka = pidva

        self.left_follower.configurePIDVA(kp, ki, kd, kv, ka)
        self.right_follower.configurePIDVA(kp, ki, kd, kv, ka)

    def update_outputs(self, l_enc: int, r_enc: int, angle: float):
        self.l_output = -self.left_follower.calculate(l_enc)
        self.r_output = self.right_follower.calculate(r_enc)

        if self.reverse:
            self.l_output = self.left_follower.calculate(-l_enc)
            self.r_output = -self.right_follower.calculate(-r_enc)
        if self.reverse:
            angle *= -1

        desired_heading = pathfinder.r2d(self.left_follower.getHeading())

        angle_diff = pathfinder.boundHalfDegrees(desired_heading - angle)
        angle_diff = angle_diff % 360
        if abs(angle_diff) > 180:
            if angle_diff > 0:
                angle_diff = angle_diff - 360
            else:
                angle_diff = angle_diff + 360

        turn = 0.8 * (1.0 / 80.0) * angle_diff
        if not self.reverse:
            self.l_output -= turn
            self.r_output -= turn
        else:
            self.l_output += turn
            self.r_output += turn


    def _path_iteration(self):
        l, r = self.get_enc()
        angle = self.get_angle()
        self.update_outputs(l, r, angle)
        self.setter(self.l_output, self.r_output)
        if self.is_finished():
            self.notifier.stop()

    def start_following(self):
        self.notifier.startPeriodic(self.left_trajectory[0].dt)

    def is_finished(self):
        return self.left_follower.isFinished() and self.right_follower.isFinished()
