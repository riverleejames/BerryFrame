"""
Test module for command classes in the BerryFrame application.

This module contains parametrized tests for various SSH command classes implemented in the 
BerryFrame application. It tests the functionality of each command class to ensure that they 
correctly execute their respective SSH commands.

The tests are designed to verify that each command class interacts properly with an SSH connection 
and executes the correct command string. This is achieved by using mock SSH connections and 
asserting the called command.

Test Data:
    test_data: A list of tuples, each representing a command class, the expected command string, and 
    any additional arguments required by the command class.

Functions:
    test_command_execute: Tests each SSH command class for correct command execution.
"""

from unittest.mock import Mock
import pytest
from commands.list_files_command import ListFilesCommand
from commands.neofetch_command import NeofetchCommand
from commands.remove_file_command import RemoveFileCommand

# Tuple format: (command_class, command_string, additional_args)
# additional_args is a dictionary of extra arguments needed for the command
test_data = [
    (ListFilesCommand, "ls -l", {}),
    (NeofetchCommand, "neofetch", {}),
    (RemoveFileCommand, "rm testfile.txt", {"filename": "testfile.txt"}),
]


@pytest.mark.parametrize("command_class, command_string, additional_args", test_data)
def test_command_execute(command_class, command_string, additional_args):
    """
    Parametrized test function to verify the execution of SSH command classes.

    This test function creates an instance of a given SSH command class with a mock SSH connection 
    and any additional arguments. It then executes the command and asserts that the correct command 
    string is passed to the SSH connection.

    Args:
        command_class (SSHCommand): The SSH command class to be tested.
        command_string (str): The expected SSH command string to be executed.
        additional_args (dict): A dictionary containing any additional arguments required for 
        initializing the command.

    The test is run for each set of parameters defined in the test_data list.
    """
    # Setup
    mock_ssh_connection = Mock()
    command = command_class(mock_ssh_connection, **additional_args)

    # Execute
    command.execute()

    # Assert
    mock_ssh_connection.execute_command.assert_called_once_with(command_string)
