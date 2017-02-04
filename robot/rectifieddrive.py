import navx
import subsystems


class RectifiedDrive:
    """
    This class implemented the rectifiedDrive function, which sets the motor outputs
    given a desired power and angular velocity using the NavX and a PID controller.
    """

    def __init__(self, kp, ki, kd, tolerance, max_input_mag, squared_inputs=True, period=0.05):
        self.kp = kp
        self.ki = ki
        self.kd = kd
        self.tolerance = abs(tolerance)  # tolerance for angular velocity of driving straight forward
        self.max_input_mag = abs(max_input_mag)  # maximum angular velocity input magnitude
        self.squared_inputs = squared_inputs  # squared inputs for angular velocity
        self.period = period

        self.prev_error = 0.0

    def rectified_drive(self, power, angular_vel):
        """
        Sets the motor outputs based on the given power and angular velocity (in degrees per second).
        """
        if self.squared_inputs:
            angular_vel = angular_vel**2 / self.max_input_mag * angular_vel / abs(angular_vel)
        if angular_vel < self.tolerance:
            angular_vel = 0
        error = navx.ahrs.getRate() - angular_vel
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
