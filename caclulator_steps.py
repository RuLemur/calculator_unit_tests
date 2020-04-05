from enum import Enum

from altunityrunner import By

from unity_driver import UnityDriver


class Operator(Enum):
    PLUS = "Plus"
    MINUS = "Minus"
    DIVISION = "Division"
    MULTIPLICATION = "Multiplication"


class CalculatorSteps(UnityDriver):

    def enter_digits(self, digits):
        for digit in list(str(digits)):
            if digit == '.':
                self.unity_driver.find_object(By.NAME, "Point").tap()
            else:
                self.unity_driver.find_object(By.NAME, digit).tap()

    def choose_operator(self, operator: Operator):
        self.unity_driver.find_object(By.NAME, operator.value).tap()

    def click_equals(self):
        self.unity_driver.find_object(By.NAME, "Equals").tap()

    def get_display_text(self):
        return self.unity_driver.find_object(By.NAME, "Text").get_text()

    def get_first_value(self):
        return self.get_display_text().split('\n')[0]

    def get_second_value(self):
        return self.get_display_text().split('\n')[2]

    def get_operator(self):
        return self.get_display_text().split('\n')[1]

    def erase_symbol(self):
        self.unity_driver.find_object(By.NAME, "EraseSymbol").tap()

    def clear_entry(self):
        self.unity_driver.find_object(By.NAME, "ClearEntry").tap()

    def clear_all(self):
        self.unity_driver.find_object(By.NAME, "ClearAll").tap()

    def change_sign(self):
        self.unity_driver.find_object(By.NAME, "ChangeSign").tap()
