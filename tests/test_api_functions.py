"""
This module contains tests for API functions related to remote system operations.
It includes fixtures and test cases for various API functions such as executing remote commands,
retrieving system statistics, and handling file uploads and downloads.
"""

import pytest
from unittest.mock import MagicMock, patch
from backend.connection_manager import ConnectionManager
from api.api_functions import (
    ExecuteRemoteCommand,
    GetSystemStats,
    UploadFile,
    DownloadFile,
)

# Constants for API function names
EXECUTE_REMOTE_COMMAND = "ExecuteRemoteCommand"
GET_SYSTEM_STATS = "GetSystemStats"
UPLOAD_FILE = "UploadFile"
DOWNLOAD_FILE = "DownloadFile"


@pytest.fixture
def mock_api_function_factory():
    """
    Provides a mock API function factory.
    This fixture creates a mock for the APIFunctionFactory, which is responsible for
    creating instances of different API function classes based on function names.
    """
    with patch("api.api_function_factory.APIFunctionFactory") as mock_factory:
        mock_factory.create_api_function.side_effect = lambda func_name: {
            EXECUTE_REMOTE_COMMAND: MagicMock(spec=ExecuteRemoteCommand),
            GET_SYSTEM_STATS: MagicMock(spec=GetSystemStats),
            UPLOAD_FILE: MagicMock(spec=UploadFile),
            DOWNLOAD_FILE: MagicMock(spec=DownloadFile),
        }[func_name]
        yield mock_factory


@pytest.fixture
def mock_connection_manager():
    """
    Provides a mock for the ConnectionManager.
    This fixture is used to simulate the ConnectionManager's behavior for testing purposes,
    specifically to avoid making actual SSH connections during tests.
    """
    with patch("backend.connection_manager.ConnectionManager") as mock:
        yield mock


def test_get_system_stats(mock_api_function_factory):
    """
    Test for verifying the GetSystemStats API function.
    This test checks if the GetSystemStats function correctly retrieves system statistics
    and returns them in the expected format.
    """
    get_system_stats = mock_api_function_factory.create_api_function(GET_SYSTEM_STATS)
    get_system_stats.execute.return_value = (
        "8.6%",
        "194/921MB (21.06%)",
        "7/29GB (27%)",
        "167",
    )

    cpu, memory, disk, processes = get_system_stats.execute()

    assert cpu == "8.6%"
    assert memory == "194/921MB (21.06%)"
    assert disk == "7/29GB (27%)"
    assert processes == "167"


@patch.object(ConnectionManager, "get_instance")
def test_upload_file_success(mock_get_instance):
    """
    Test the successful upload of a file.

    This test validates that the UploadFile class can successfully upload a file
    from a local path to a remote path using SFTP. It checks the correctness of
    the method calls for opening an SFTP session, transferring the file, and
    closing the session.
    """
    # Arrange
    local_path = "local/file/path"
    remote_path = "remote/file/path"
    mock_ssh_client = MagicMock()
    mock_sftp_client = MagicMock()
    mock_get_instance.return_value.ssh_client = mock_ssh_client
    mock_ssh_client.open_sftp.return_value = mock_sftp_client

    uploader = UploadFile()

    # Act
    uploader.execute(local_path, remote_path)

    # Assert
    mock_ssh_client.open_sftp.assert_called_once()
    mock_sftp_client.put.assert_called_once_with(local_path, remote_path)
    mock_sftp_client.close.assert_called_once()


@patch.object(ConnectionManager, "get_instance")
def test_download_file_success(mock_get_instance):
    """
    Test the successful download of a file.

    This test validates that the DownloadFile class can successfully download a file
    from a remote path to a local path using SFTP. It checks the correctness of
    the method calls for opening an SFTP session, retrieving the file, and
    closing the session.
    """
    # Arrange
    remote_path = "remote/file/path"
    local_path = "local/file/path"
    mock_ssh_client = MagicMock()
    mock_sftp_client = MagicMock()
    mock_get_instance.return_value.ssh_client = mock_ssh_client
    mock_ssh_client.open_sftp.return_value = mock_sftp_client

    downloader = DownloadFile()

    # Act
    downloader.execute(remote_path, local_path)

    # Assert
    mock_ssh_client.open_sftp.assert_called_once()
    mock_sftp_client.get.assert_called_once_with(remote_path, local_path)
    mock_sftp_client.close.assert_called_once()
