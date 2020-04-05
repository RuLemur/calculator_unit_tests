import unittest

from altunityrunner import AltrunUnityDriver, AltUnityAndroidPortForwarding
from appium import webdriver

CAPS = {
    'platformName': 'Android',
    'appPackage': 'com.Banzai.QATestTask',
    'deviceName': 'auto',
    'appActivity': 'com.unity3d.player.UnityPlayerActivity',
    'noReset': True,
    'newCommandTimeout': 360
}


class UnityDriver(unittest.TestCase):

    def setUp(self):
        self.forwarding = AltUnityAndroidPortForwarding()
        self.forwarding.remove_all_forwards()
        self.forwarding.forward_port_device()

        self.appium_driver = webdriver.Remote('http://localhost:4723/wd/hub', CAPS)
        self.wait_for_alt_unity_server()
        self.unity_driver = AltrunUnityDriver(self.appium_driver, 'android')

    def wait_for_alt_unity_server(self):
        device = self.forwarding.get_device()
        device.shell("logcat -c")
        device.shell("logcat -s Unity", handler=self.wait_handler)

    @staticmethod
    def wait_handler(connect):
        file_obj = connect.socket.makefile()
        for line in file_obj:
            if "AltUnity Driver started" in line:
                break
        file_obj.close()
        connect.close()

    def tearDown(self):
        self.unity_driver.stop()
        self.appium_driver.quit()
        self.forwarding.remove_all_forwards()
