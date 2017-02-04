import navx
import subsystems


class RectifiedDrive:
    """
    This class implemented the rectifiedDrive function, which sets the motor outputs
    given a desired power and angular velocity using the NavX and a PID controller.
    """

    def __init__(self, kp, ki, kd, period=0.05):
        self.kp = kp
        self.ki = ki
        self.kd = kd
        self.period = period

        self.prev_error = 0.0

    def rectifiedDrive(self, power, angular_vel):
        error = angular_vel - navx.ahrs.getRate()
        output = self.calc_pid(error)
        left_output = power - output
        if abs(left_output) > 1.0:  # normalize if magnitude greater than 1
            left_output /= abs(left_output)
        right_output = power + output
        if abs(right_output) > 1.0:  # normalize if magnitude greater than 1
            right_output /= abs(right_output)
        subsystems.motors.robot_drive.setLeftRightMotorOutputs(left_output, right_output)

    def calc_pid(self, error):
        e_deriv = (error - self.prev_error) / self.period
        e_int = (error + self.prev_error) / 2 * self.period
        self.prev_error = error
        return self.kp * error + self.kd * e_deriv + self.ki * e_int
