import sys
from calculator.operations import Operations
from calculator.calculation import ArithmeticCalculation
from calculator.commands import CalculateCommand, HistoryCommand

def main():
    history = []
    operations_map = {
        "add": Operations.add,
        "subtract": Operations.subtract,
        "multiply": Operations.multiply,
        "divide": Operations.divide,
    }

    while True:
        try:
            line = input(">>> ")
        except (KeyboardInterrupt, EOFError):
            print()
            break

        parts = line.strip().split()
        if not parts:
            continue

        command_name = parts[0].lower()

        if command_name == "exit":
            break

        if command_name == "history":
            cmd = HistoryCommand(history)
            h_list = cmd.execute()
            if not h_list:
                print("History is empty.")
            else:
                for item in h_list:
                    print(item)
            continue

        if command_name in operations_map:
            if len(parts) != 3:
                print("Error: Missing or extra operands. Usage: <operation> <a> <b>")
                continue
            try:
                a = float(parts[1])
                b = float(parts[2])
            except ValueError:
                print("Error: Invalid numbers.")
                continue

            try:
                op_func = operations_map[command_name]
                calc = ArithmeticCalculation.create(a, b, op_func)
                cmd = CalculateCommand(calc, history)
                result = cmd.execute()
                print(result)
            except ValueError as e:
                print(f"Error: {e}")
            continue

        print(f"Unknown command: {command_name}")

if __name__ == "__main__":  # pragma: no cover
    main()