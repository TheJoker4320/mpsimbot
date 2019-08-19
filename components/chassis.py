from ctre import WPI_TalonSRX, FeedbackDevice, ControlMode
from wpilib.drive import DifferentialDrive
from navx import AHRS

class Chassis:
    left_master: WPI_TalonSRX
    left_slave: WPI_TalonSRX
    right_master: WPI_TalonSRX
    right_slave: WPI_TalonSRX
    navx: AHRS

    def __init__(self):
        pass

    def setup(self):
        self.left_slave.follow(self.left_master)
        self.right_slave.follow(self.right_master)

        self.left_master.configSelectedFeedbackSensor(FeedbackDevice.QuadEncoder)
        self.right_master.configSelectedFeedbackSensor(FeedbackDevice.QuadEncoder)

        self.left_master.configVoltageCompSaturation(11)
        self.right_master.configVoltageCompSaturation(11)

        self.left_master.enableVoltageCompensation(True)
        self.right_master.enableVoltageCompensation(True)

        self.diff_drive = DifferentialDrive(self.left_master, self.right_master)

    def arcade_drive(self, y_speed: float, z_speed: float):
        self.diff_drive.arcadeDrive(y_speed, z_speed)

    def tank_drive(self, left_speed: float, right_speed: float):
        self.diff_drive.tankDrive(left_speed, right_speed)

    def get_encoder_ticks(self):
        left_pos = self.left_master.getSelectedSensorPosition()
        right_pos = self.right_master.getSelectedSensorPosition()

        return left_pos, right_pos

    def set_motors_value(self,left: float, right: float):
        self.left_master.set(left, ControlMode.PercentOutput)
        self.right_master.set(right, ControlMode.PercentOutput)

    def reset_encoders(self):
        self.left_master.setSelectedSensorPosition(0)
        self.right_master.setSelectedSensorPosition(0)

    def get_angle(self):
        return self.navx.getAngle()

    def reset_angle(self):
        self.navx.zeroYaw()