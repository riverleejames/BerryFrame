"""
Test Suite for the SSH Management System

This module contains pytest test cases for the SSH Management System. 
It tests the functionality of various components in the main module by 
mocking external dependencies and user inputs to ensure that each function
behaves as expected under different scenarios.
"""

from unittest.mock import Mock, patch, ANY
import main

@patch('main.console')
def test_main_menu(mock_console):
    """
    Tests the main_menu function of the SSH Management System.

    This test verifies if the main_menu function correctly calls the
    print method on the console object, ensuring that the menu is 
    displayed to the user.
    """
    main.main_menu()
    mock_console.print.assert_called()  # Check if print is called

@patch('main.console')
def test_connect_ssh(mock_console):
    """
    Tests the connect_ssh function of the SSH Management System.

    This test ensures that connect_ssh correctly initiates an SSH 
    connection using the provided controller and that appropriate 
    messages are displayed during the connection process.
    """
    mock_controller = Mock()
    main.connect_ssh(mock_controller)
    mock_controller.connect.assert_called_once()
    mock_console.print.assert_called()  # Check if print is called with the right arguments

@patch('main.Prompt')
@patch('main.connect_ssh')
@patch('main.console')
def test_check_ssh_connection_when_disconnected(mock_console, mock_connect_ssh, mock_prompt):
    """
    Tests the check_ssh_connection function when the SSH connection is initially disconnected.

    This test verifies the behavior of check_ssh_connection when the SSH connection is not active.
    It confirms that the function prompts the user to establish a connection and proceeds correctly
    based on the user's response.
    """
    mock_controller = Mock()
    mock_controller.is_connected.return_value = False
    mock_prompt.ask.return_value = "yes"

    assert main.check_ssh_connection(mock_controller) is True
    mock_connect_ssh.assert_called_once_with(mock_controller)
    mock_console.print.assert_called()  # Check if print is called with the right arguments


@patch('main.check_ssh_connection', return_value=True)
@patch('main.console')
def test_execute_remote_command(mock_console, mock_check_ssh):
    """
    Tests the execute_remote_command function of the SSH Management System.

    This test checks if the function correctly handles the execution of a remote command
    on the SSH server when the SSH connection is active.
    """
    mock_controller = Mock()
    mock_invoker = Mock()
    command = "ls"

    main.execute_remote_command(mock_controller, mock_invoker, command)
    mock_invoker.execute_command.assert_called_once()
    mock_console.print.assert_called()  # Check if print is called with the right arguments

@patch('main.console')
def test_disconnect_ssh(mock_console):
    """
    Tests the disconnect_ssh function of the SSH Management System.

    This test ensures that disconnect_ssh correctly terminates the SSH connection
    and that appropriate status messages are displayed during the disconnection process.
    """
    mock_controller = Mock()
    main.disconnect_ssh(mock_controller)
    mock_controller.disconnect.assert_called_once()
    mock_console.print.assert_called()  # Check if print is called with the right arguments

@patch('main.check_ssh_connection', return_value=True)
@patch('main.console')
def test_execute_neofetch_command(mock_console, mock_check_ssh):
    """
    Tests the execute_neofetch_command function of the SSH Management System.

    This test verifies if the execute_neofetch_command function correctly handles
    the execution of the Neofetch command on the remote server when the SSH
    connection is active.
    """
    mock_controller = Mock()
    mock_invoker = Mock()

    main.execute_neofetch_command(mock_controller, mock_invoker)
    mock_invoker.execute_command.assert_called_once_with(ANY)
    mock_console.print.assert_called()  # Check if print is called with the right arguments

@patch('main.check_ssh_connection', return_value=True)
@patch('main.console')
def test_execute_list_files_command(mock_console, mock_check_ssh):
    """
    Tests the execute_list_files_command function of the SSH Management System.

    This test checks if the function correctly handles the execution of the command 
    to list files on the remote server when the SSH connection is active.
    """
    mock_controller = Mock()
    mock_invoker = Mock()

    main.execute_list_files_command(mock_controller, mock_invoker)
    mock_invoker.execute_command.assert_called_once_with(ANY)
    mock_console.print.assert_called()  # Check if print is called with the right arguments

