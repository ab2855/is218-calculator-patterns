import pytest
from calculator.operations import Operations
from calculator.calculation import ArithmeticCalculation
from calculator.commands import CalculateCommand, HistoryCommand
from calculator.cli import main

def test_subtract():
    assert Operations.subtract(5, 3) == 2

def test_multiply():
    assert Operations.multiply(4, 3) == 12

def test_divide():
    assert Operations.divide(6, 3) == 2.0

def test_divide_by_zero():
    with pytest.raises(ValueError, match="Cannot divide by zero"):
        Operations.divide(5, 0)

def test_calculate_command_and_history():
    history = []
    calc = ArithmeticCalculation.create(10, 5, Operations.add)
    cmd = CalculateCommand(calc, history)
    result = cmd.execute()
    assert result == 15
    assert len(history) == 1

    history_cmd = HistoryCommand(history)
    h_copy = history_cmd.execute()
    assert len(h_copy) == 1
    
    # Ensure history copy is isolated
    h_copy.append("fake entry")
    assert len(history) == 1

def test_cli_add_and_exit(monkeypatch, capsys):
    inputs = iter(["add 5 3", "exit"])
    monkeypatch.setattr("builtins.input", lambda prompt="": next(inputs))
    main()
    captured = capsys.readouterr()
    assert "8" in captured.out

def test_cli_history_commands(monkeypatch, capsys):
    # Test empty history first, then add something and check history
    inputs = iter(["history", "add 10 2", "history", "exit"])
    monkeypatch.setattr("builtins.input", lambda prompt="": next(inputs))
    main()
    captured = capsys.readouterr()
    assert "History is empty." in captured.out
    assert "10" in captured.out

def test_cli_error_handling(monkeypatch, capsys):
    inputs = iter([
        "badcommand",      # Unknown command
        "add 5",           # Missing operand
        "add 5 3 2",       # Extra operands
        "add abc 3",       # Invalid number
        "divide 5 0",      # Division by zero
        "",                # Empty line
        "exit"
    ])
    monkeypatch.setattr("builtins.input", lambda prompt="": next(inputs))
    main()
    captured = capsys.readouterr()
    assert "Unknown command" in captured.out
    assert "Missing or extra operands" in captured.out
    assert "Invalid numbers" in captured.out
    assert "Cannot divide by zero" in captured.out

def test_cli_eof_handling(monkeypatch, capsys):
    def mock_input(prompt=""):
        raise EOFError()
    monkeypatch.setattr("builtins.input", mock_input)
    main()  # Should break cleanly on EOF