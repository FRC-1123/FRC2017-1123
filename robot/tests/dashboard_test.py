from pyfrc.test_support import controller
import robotmap

from networktables import NetworkTables


def test_dashButton(hal_data: controller.hal_data, control: controller.TestController, fake_time, robot):
    def tController(t):
        table = NetworkTables.getTable("SmartDashboard")
        if t < 2:
            table.putBoolean("forwardCommand", True)
        elif t < 5:
            table.putBoolean("turnCommand", True)
        else:
            return False
        return True

    control.set_operator_control(enabled=True)
    control.run_test(tController)
    assert int(fake_time.get()) == 5
