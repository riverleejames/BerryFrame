"""
This module contains unit tests for the functions in the api_functions module.
It tests the functionality of remote command execution, system stats retrieval,
and file upload and download operations.
"""

from unittest.mock import patch, MagicMock
import pytest
from backend.api_functions import (
    execute_remote_command,
    get_system_stats,
    upload_file,
    download_file,
)

@pytest.fixture
def mock_connection_manager():
    """
    A pytest fixture that mocks the ConnectionManager class.
    This mock is used to simulate the behavior of the ConnectionManager
    without making actual SSH connections.

    Yields:
        MagicMock: The mocked ConnectionManager class.
    """
    with patch("backend.api_functions.ConnectionManager") as mock:
        yield mock


def test_execute_remote_command(mock_connection_manager):
    """
    Test the execute_remote_command function to verify if it correctly handles
    the execution of commands using the ConnectionManager.

    Args:
        mock_connection_manager (MagicMock): Mocked ConnectionManager fixture.
    """
    # Setup the mock to return a specific output
    mock_connection_manager.get_instance.return_value.execute_command.return_value = (
        "output"
    )

    # Execute the function with a test command
    result = execute_remote_command("command")

    # Assert that the result matches the mock output
    assert result == "output"


def test_get_system_stats(mocker):
    """
    Test the get_system_stats function to ensure it correctly aggregates system
    statistics by calling the execute_remote_command function with specific commands.

    Args:
        mocker (pytest_mock.MockFixture): Pytest's mocker fixture for mocking objects.
    """
    # Mock the execute_remote_command function
    mocked_execute = mocker.patch("backend.api_functions.execute_remote_command")

    # Define mock outputs for specific commands
    mocked_execute.side_effect = lambda command: {
        "top -bn1 | grep 'Cpu(s)' | awk '{print $2+$4}'": "8.6%",
        "free -m | awk 'NR==2{printf \"Memory Usage: %s/%sMB (%.2f%%)\", $3,$2,$3*100/$2 }'": "194/921MB (21.06%)",
        'df -h | awk \'$NF=="/"{printf "Disk Usage: %d/%dGB (%s)", $3,$2,$5}\'': "7/29GB (27%)",
        "ps -e | wc -l": "167",
    }[command]

    # Call the function and get the results
    cpu_usage, memory_usage, disk_space, running_processes = get_system_stats()

    # Assert the function returns the expected values
    assert cpu_usage == "8.6%"
    assert memory_usage == "194/921MB (21.06%)"
    assert disk_space == "7/29GB (27%)"
    assert running_processes == "167"


def test_upload_file(mock_connection_manager):
    """
    Test the upload_file function to ensure it correctly handles file uploads
    using SFTP through the ConnectionManager.

    Args:
        mock_connection_manager (MagicMock): Mocked ConnectionManager fixture.
    """
    mock_sftp_client = MagicMock()
    # Setup mock SFTP client
    mock_connection_manager.get_instance.return_value.ssh_client.open_sftp.return_value = (
        mock_sftp_client
    )

    # Call upload_file function
    upload_file("/local/path", "/remote/path")

    # Assert that the SFTP client's put method was called correctly
    mock_sftp_client.put.assert_called_once_with("/local/path", "/remote/path")
    # Assert that the SFTP client is closed after operation
    mock_sftp_client.close.assert_called_once()


def test_download_file(mock_connection_manager):
    """
    Test the download_file function to ensure it correctly handles file downloads
    using SFTP through the ConnectionManager.

    Args:
        mock_connection_manager (MagicMock): Mocked ConnectionManager fixture.
    """
    mock_sftp_client = MagicMock()
    # Setup mock SFTP client
    mock_connection_manager.get_instance.return_value.ssh_client.open_sftp.return_value = (
        mock_sftp_client
    )

    # Call download_file function
    download_file("/remote/path", "/local/path")

    # Assert that the SFTP client's get method was called correctly
    mock_sftp_client.get.assert_called_once_with("/remote/path", "/local/path")
    # Assert that the SFTP client is closed after operation
    mock_sftp_client.close.assert_called_once()
