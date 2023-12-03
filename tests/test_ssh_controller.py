"""
Module for testing the SSHController class.

This module contains a suite of tests designed to verify the functionality of the 
SSHController class, which is responsible for managing SSH connections and interacting 
with the view component. The tests employ mock objects to simulate the behavior of the
controller's dependencies and assert the correct interaction between these components.

Tests in this module cover:
- Initialization of the SSHController with proper observer attachment.
- Functionality of the `connect` method, ensuring it invokes the ConnectionManager's 
  connect method correctly.
- Functionality of the `disconnect` method, ensuring it calls the ConnectionManager's 
  disconnect method.

The tests use the pytest framework for setup and execution, employing fixtures for 
common test setup tasks. Mock objects are used extensively to isolate the controller 
from its dependencies, allowing for focused and reliable testing of the controller's behavior.

Functions:
    reset_connection_manager: A pytest fixture to reset the connection manager before each test.
    mock_connection_manager: A pytest fixture to provide a mock connection manager.
    mock_view: A pytest fixture to provide a mock view object.
    mock_factory: A pytest fixture to provide a mock API function factory.
    ssh_controller: A pytest fixture to create an SSHController instance with mock dependencies.
    test_initialization: Tests the initialization of SSHController.
    test_connect: Tests the `connect` method of SSHController.
    test_disconnect: Tests the `disconnect` method of SSHController.

Example:
    To run these tests, ensure pytest is installed and execute `pytest` in the directory 
    containing this module.

Note:
    The tests assume the presence of a `config.ini` file with valid SSH connection details. 
    Ensure this file is correctly set up and accessible to the test environment.
"""

from unittest.mock import patch

import pytest

from controllers.ssh_controller import SSHController


@pytest.fixture(autouse=True)
def reset_connection_manager():
    """
        A pytest fixture that resets the ConnectionManager's instance before each test.

        This fixture is automatically used for every test function in this module. It patches
        the ConnectionManager's reset_instance method to ensure that each test starts with a fresh
        instance of the ConnectionManager, thereby avoiding shared state across tests.

        Yields:
            None
    """
    with patch("model.backend.connection_manager.ConnectionManager.reset_instance"):
        yield


@pytest.fixture
def mock_connection_manager():
    """
        A pytest fixture that provides a mock of the ConnectionManager.

        This fixture creates a mock for the ConnectionManager.get_instance method, allowing tests
        to simulate and control the behavior of the ConnectionManager without making actual 
        SSH connections.

        Yields:
            MagicMock: A mock object representing an instance of ConnectionManager.
        """
    with patch("model.backend.connection_manager.ConnectionManager.get_instance") as mock:
        yield mock.return_value


@pytest.fixture
def mock_view():
    """
    A pytest fixture that provides a mock of the SSHView class.

    This fixture creates a mock for the SSHView class, enabling tests to verify interactions
    between the SSHController and the view component without needing a real view implementation.

    Yields:
        MagicMock: A mock object representing an instance of SSHView.
    """
    with patch("views.ssh_view.SSHView") as mock:
        yield mock.return_value


@pytest.fixture
def mock_factory():
    """
    A pytest fixture that provides a mock of the APIFunctionFactory.

    This fixture sets up a mock for the APIFunctionFactory, used by the SSHController for
    creating API function instances. It allows tests to control and inspect the use of API functions
    within the SSHController.

    Yields:
        MagicMock: A mock object representing an instance of APIFunctionFactory.
    """
    with patch("model.api.api_function_factory.APIFunctionFactory") as mock:
        yield mock.return_value


@pytest.fixture
def ssh_controller(mock_connection_manager, mock_view, mock_factory):
    """
    A pytest fixture that creates an instance of SSHController with mocked dependencies.

    This fixture constructs an SSHController object using mocked instances of the ConnectionManager,
    SSHView, and APIFunctionFactory. It is used to test the SSHController's methods in 
    isolation from its external dependencies.

    Args:
        mock_connection_manager (MagicMock): The mock connection manager instance.
        mock_view (MagicMock): The mock SSH view instance.
        mock_factory (MagicMock): The mock API function factory instance.

    Returns:
        SSHController: An instance of SSHController with mocked dependencies.
    """
    return SSHController("host", 22, "username", "password", "key_path", view=mock_view)


def test_initialization(ssh_controller, mock_connection_manager):
    """
    Tests the initialization process of the SSHController.

    This test verifies that the SSHController correctly attaches itself as an observer to the
    ConnectionManager during its initialization. The test checks the number of times the 
    attach method is called on the mock ConnectionManager.

    Args:
        ssh_controller (SSHController): The SSHController instance to be tested.
        mock_connection_manager (MagicMock): The mocked ConnectionManager instance.

    Asserts:
        The attach method of the mock ConnectionManager is called the expected number of times.
    """
    assert mock_connection_manager.attach.call_count == 2


def test_connect(ssh_controller, mock_connection_manager, mock_view):
    """
    Test the connect method of the SSH controller.

    This test verifies that the `connect` method of the SSH controller correctly calls the 
    `connect` method of the connection manager with the expected parameters and shows the 
    appropriate message on the view.

    Args:
        ssh_controller (obj): The SSH controller object.
        mock_connection_manager (obj): The mock connection manager object.
        mock_view (obj): The mock view object.

    Returns:
        None
    """
    ssh_controller.connect()
    mock_connection_manager.connect.assert_called_with("host", 22, "username", "password",
                                                        "key_path")
    mock_view.show_message.assert_called_with("Connected to host")


def test_disconnect(ssh_controller, mock_connection_manager, mock_view):
    """
    Test the disconnect method of the SSH controller.

    This test verifies that the `disconnect` method of the SSH controller correctly calls 
    the `disconnect` method of the connection manager and shows the appropriate message 
    on the view.

    Args:
        ssh_controller (obj): The SSH controller object.
        mock_connection_manager (obj): The mock connection manager object.
        mock_view (obj): The mock view object.
    """
    ssh_controller.disconnect()
    mock_connection_manager.disconnect.assert_called_once()
    mock_view.show_message.assert_called_with("Disconnected")
