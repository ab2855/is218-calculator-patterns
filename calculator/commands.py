from calculator.calculation import Calculation

class CalculateCommand:
    def __init__(self, calculation: Calculation, history: list):
        self.calculation = calculation
        self.history = history

    def execute(self) -> float:
        result = self.calculation.execute()
        entry = f"{self.calculation.a} {self.calculation.operation.__name__} {self.calculation.b} = {result}"
        self.history.append(entry)
        return result

class HistoryCommand:
    def __init__(self, history: list):
        self.history = history

    def execute(self) -> list:
        return self.history.copy()