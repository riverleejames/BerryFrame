"""
Test module for SSHCommandInvoker in the BerryFrame application.

This module contains tests for SSHCommandInvoker, focusing on its ability to execute SSH commands
and maintain a history of executed commands. The tests ensure that the invoker correctly executes
commands using mock SSHCommand instances and accurately tracks the history of these commands.

Functions:
    test_execute_command: Verifies that the SSHCommandInvoker correctly executes a command and 
    records it in history. 
    test_show_history: Tests the functionality of the SSHCommandInvoker's show_history method.
"""

from unittest.mock import create_autospec
from commands.ssh_command import SSHCommand
from controllers.command_invoker import SSHCommandInvoker

def test_execute_command():
    """
    Test to ensure that SSHCommandInvoker correctly executes a command and records it in history.

    This test verifies that the execute_command method of SSHCommandInvoker calls the execute method 
    of a given SSH command and then adds the command to its history. It uses a mock SSHCommand to 
    avoid actual SSH operations.

    Assertions:
        - The execute method of the mock command is called once.
        - The command invoker's history contains one record.
        - The command in the history is the same as the mock command executed.
    """
    # Setup
    mock_command = create_autospec(SSHCommand)
    invoker = SSHCommandInvoker()

    # Execute
    invoker.execute_command(mock_command)

    # Assert
    mock_command.execute.assert_called_once()
    assert len(invoker.history) == 1
    assert invoker.history[0][0] == mock_command


def test_show_history(capsys):
    """
    Test the functionality of the show_history method of SSHCommandInvoker.

    This test checks that the show_history method correctly outputs the history of executed 
    commands. It uses mock SSHCommand instances, with specified return values for their execute 
    methods, to simulate the execution of commands and capture the output using the capsys fixture.

    Assertions:
        - The output contains the string "Executed: " indicating that history is being displayed.
        - The output includes the specified return values of the executed mock commands.
    """
    # Setup
    mock_command1 = create_autospec(SSHCommand)
    mock_command2 = create_autospec(SSHCommand)

    # Configure mocks to return specific values when execute() is called
    mock_command1.execute.return_value = 'Result 1'
    mock_command2.execute.return_value = 'Result 2'

    invoker = SSHCommandInvoker()

    # Execute
    invoker.execute_command(mock_command1)
    invoker.execute_command(mock_command2)
    invoker.show_history()

    # Assert
    captured = capsys.readouterr()
    assert "Executed: " in captured.out
    assert "Result 1" in captured.out
    assert "Result 2" in captured.out
