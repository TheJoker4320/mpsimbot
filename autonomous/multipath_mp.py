from magicbot import state, timed_state

from autonomous.motion_profile_state_machine import MotionProfileStateMachine


class MultiPathMP(MotionProfileStateMachine):
    MODE_NAME = "multi"
    DEFAULT = True

    @timed_state(duration=3,next_state="rocket_to_loading")
    def wait(self):
        pass
    @state(first=True)
    def hub_to_rocket(self, initial_call):
        if initial_call:
            self.create_path_follower("hubToRocket", 0.02, 0, 0)
            self.path_follower.start_following()

        if self.path_follower.is_finished():
            print("finished 1")
            self.chassis.reset_encoders()
            self.chassis.reset_angle()
            self
            self.next_state("wait")

    @state
    def rocket_to_loading(self, initial_call):
        if initial_call:
            self.create_path_follower("rocketToLoading", 0.01, 0, 0, reverse=True)
            self.path_follower.start_following()

        if self.path_follower.is_finished():
            print("finished 2")
            self.chassis.reset_encoders()
            self.chassis.reset_angle()
            self.next_state("loading_to_rocket")

    @state
    def loading_to_rocket(self, initial_call):
        if initial_call:
            self.create_path_follower("loadingToRocket", 0.02, 0, 0)
            self.path_follower.start_following()

        if self.path_follower.is_finished():
            print("finished all")
            self.chassis.reset_encoders()
            self.chassis.reset_angle()
            super().done()
