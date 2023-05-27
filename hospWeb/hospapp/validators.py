from django.core.validators import BaseValidator


class MaxPhoneValid(BaseValidator):
    message = "Убедитесь в правильности ввода номера"
    code = "max_value"

    def compare(self, a, b):
        return a > b


class MinPhoneValid(BaseValidator):
    message = "Убедитесь в правильности ввода номера"
    code = "min_value"

    def compare(self, a, b):
        return a < b
