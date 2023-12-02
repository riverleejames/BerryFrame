"""
This module contains unit tests for the ConnectionManager class.
"""
from unittest.mock import patch, MagicMock

import paramiko
import pytest

from model.backend.connection_manager import ConnectionManager, Observer


@pytest.fixture(autouse=True)
def reset_connection_manager():
    """
    Pytest fixture to reset ConnectionManager before each test.
    """
    ConnectionManager.reset_instance()
    yield
    ConnectionManager.reset_instance()


def test_singleton_instance():
    """
    Test that ConnectionManager returns the same instance for multiple get_instance() calls.
    This ensures that the ConnectionManager class follows the Singleton design pattern.
    """
    manager1 = ConnectionManager.get_instance()
    manager2 = ConnectionManager.get_instance()
    assert manager1 is manager2


def test_initialization():
    """
    Test the initialization of the ConnectionManager class.
    This test verifies that a Paramiko SSHClient is created
    when the ConnectionManager is initialized.
    """
    with patch("paramiko.SSHClient") as mock_ssh:
        _ = ConnectionManager.get_instance()
        mock_ssh.assert_called_once()

        # Check if AutoAddPolicy is used for the set_missing_host_key_policy method
        _, args, _ = mock_ssh.return_value.set_missing_host_key_policy.mock_calls[0]
        assert isinstance(args[0], paramiko.AutoAddPolicy)


def test_ssh_connection():
    """
    Test the establishment of an SSH connection through the ConnectionManager.
    This test ensures that the SSH connect method is called with the correct parameters.
    """
    test_host = "test_host"
    test_port = 22
    test_username = "user"
    test_password = "pass"
    test_key_path = "/path/to/key"

    manager = ConnectionManager.get_instance()

    with patch.object(manager, "ssh_client", new_callable=MagicMock) as mock_ssh_client:
        manager.connect(
            test_host, test_port, test_username, test_password, test_key_path
        )

        mock_ssh_client.connect.assert_called_with(
            test_host,
            test_port,
            username=test_username,
            password=test_password,
            key_filename=test_key_path,
        )


def test_disconnect():
    """
    Test the disconnection process of the ConnectionManager.
    This test checks if the close method of the SSH client is called upon disconnection.
    """
    manager = ConnectionManager.get_instance()

    with patch.object(manager, "ssh_client", new_callable=MagicMock) as mock_ssh_client:
        manager.disconnect()
        mock_ssh_client.close.assert_called_once()


def test_execute_command():
    """
    Test the execution of a command through the ConnectionManager.
    This test ensures that the exec_command method of SSH client is called and
    returns the expected output.
    """
    command = "ls -l"
    expected_output = "mocked output"

    manager = ConnectionManager.get_instance()

    with patch.object(manager, "ssh_client", new_callable=MagicMock) as mock_ssh_client:
        mock_ssh_client.exec_command.return_value = (
            MagicMock(),
            MagicMock(),
            MagicMock(),
        )
        mock_stdout = mock_ssh_client.exec_command.return_value[1]
        mock_stdout.read.return_value = expected_output.encode()

        output = manager.execute_command(command)

        assert output == expected_output
        mock_ssh_client.exec_command.assert_called_with(command)


def test_observer_notification_on_connect():
    """
    Test that observers are notified with the correct status when a connection is established.
    """
    observer_mock = MagicMock(spec=Observer)
    manager = ConnectionManager.get_instance()
    manager.attach(observer_mock)

    with patch.object(manager, "ssh_client", new_callable=MagicMock) as mock_ssh_client:
        mock_ssh_client.connect.return_value = None
        manager.connect("host", 22, "user", "pass", "")

        observer_mock.update.assert_called_once_with("Connected")


def test_observer_notification_on_disconnect():
    """
    Test that observers are notified of the correct status when a connection is terminated.
    """
    observer_mock = MagicMock(spec=Observer)
    manager = ConnectionManager.get_instance()
    manager.attach(observer_mock)

    with patch.object(manager, "ssh_client", new_callable=MagicMock) as mock_ssh_client:
        mock_ssh_client.connect.return_value = None
        manager.connect("host", 22, "user", "pass", "")

        mock_ssh_client.close.return_value = None
        manager.disconnect()

        observer_mock.update.assert_called_with("Disconnected")
