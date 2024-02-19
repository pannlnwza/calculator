import math


class Model:
    """Model class for the calculator application."""
    def __init__(self):
        self.history = []

    def update_history(self, user_input, result):
        """Update the calculation history with the latest calculation."""
        self.history.append(f"{user_input}={result:.7g}")

    def clear_history(self):
        """Clear the calculation history."""
        self.history = []

    def calculate(self, user_input):
        """Perform the calculation based on the input."""
        replacement = {"exp": "math.exp",
                       "ln": "math.log",
                       "log10": "math.log10",
                       "log2": "math.log2",
                       "sqrt": "math.sqrt",
                       "^": "**",
                       "mod": "%"}
        try:
            for key, value in replacement.items():
                user_input = user_input.replace(key, str(value))
            result = eval(user_input)
            return result
        except SyntaxError:
            return None
        except ZeroDivisionError:
            return None
