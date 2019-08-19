from wpilib import Talon

class MyComponent:
    """Basic componenets example"""
    motor: Talon

    def __init__(self):
        """
        C'tor for the components.
        Injected variables are not yet injected, to deal with them use the 'setup' function
        """
        pass

    def setup(self):
        pass

    def execute(self):
        self.motor.set(1)