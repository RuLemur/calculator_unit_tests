from parameterized import parameterized

from caclulator_steps import CalculatorSteps, Operator


class CalculatorTest(CalculatorSteps):

    @parameterized.expand([
        [Operator.PLUS, "56", "33", "89"],
        [Operator.MINUS, "24", "15", "9"],
        [Operator.DIVISION, "10", "5", "2"],
        [Operator.MULTIPLICATION, "14", "3", "42"],
        [Operator.PLUS, "14.4", "3.4", "17.8"],
        [Operator.MINUS, "43.2", "3.4", "39.8"],
        [Operator.DIVISION, "7", "2", "3.5"],
        [Operator.MULTIPLICATION, "7.1", "3", "21.3"],
    ])
    def test_simple_operations(self, operator, first, second, result):
        self.enter_digits(first)
        self.choose_operator(operator)
        self.enter_digits(second)
        self.click_equals()
        assert self.get_first_value() == result

    def test_oversize_int(self,):
        self.enter_digits(2147483647)
        self.choose_operator(Operator.PLUS)
        self.enter_digits(1)
        self.click_equals()
        assert self.get_first_value() == "2.147484E+09"

    def test_infinity(self):
        self.enter_digits(9999999999999999999999)
        self.choose_operator(Operator.MULTIPLICATION)
        self.enter_digits(9999999999999999999999)
        self.click_equals()
        assert self.get_first_value() == "Infinity"

    def test_type_after_infinity(self):
        self.enter_digits(9999999999999999999999)
        self.choose_operator(Operator.MULTIPLICATION)
        self.enter_digits(9999999999999999999999)
        self.click_equals()
        self.enter_digits(1234)
        assert self.get_first_value() == "1234"

    def test_divide_by_zero(self):
        self.enter_digits(123)
        self.choose_operator(Operator.DIVISION)
        self.enter_digits(0)
        self.click_equals()
        assert self.get_first_value() == "Infinity"

    def test_change_sign(self):
        self.enter_digits(123)
        self.change_sign()
        self.choose_operator(Operator.PLUS)
        self.enter_digits(123)
        self.click_equals()
        assert self.get_first_value() == "0"

    def test_erase(self):
        self.enter_digits(123)
        self.erase_symbol()
        assert self.get_first_value() == "12"

    def test_erase_second_value(self):
        self.enter_digits(123)
        self.choose_operator(Operator.PLUS)
        self.enter_digits(432)
        self.erase_symbol()
        assert self.get_first_value() == "123"
        assert self.get_second_value() == "43"

    def test_clear_entry(self):
        self.enter_digits(123)
        self.clear_entry()
        assert self.get_first_value() == "0"

    def test_clear_second_entry(self):
        self.enter_digits(123)
        self.choose_operator(Operator.PLUS)
        self.enter_digits(432)
        self.clear_entry()
        assert self.get_first_value() == "123"
        assert self.get_operator() == "+"
        assert self.get_second_value() == "0"

    def test_clear_all(self):
        self.enter_digits(144)
        self.choose_operator(Operator.DIVISION)
        self.enter_digits(87)
        self.clear_all()
        assert self.get_first_value() == "0"
        assert self.get_operator() == ""
        assert self.get_second_value() == ""

    def test_multiply_digits(self):
        self.enter_digits("14.24..4")
        assert self.get_first_value() == "14.244"

    def test_all_digit_buttons(self):
        self.enter_digits(987654321)
        self.choose_operator(Operator.MINUS)
        self.enter_digits(987654321)
        self.click_equals()
        assert self.get_first_value() == "0"

    def test_change_operation(self):
        self.enter_digits(321)
        self.choose_operator(Operator.MINUS)
        self.enter_digits(422)
        assert self.get_operator() == "-"
        self.choose_operator(Operator.PLUS)
