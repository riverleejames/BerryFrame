"""
Unit tests for the AlertSystem class in the observer module.

This module contains unit tests for the AlertSystem class, 
specifically testing its update method. The tests ensure that the 
AlertSystem correctly handles and responds to status updates, 
such as changes in network status. These tests use the Python 
unittest framework and include the use of mock objects to simulate 
and verify the behavior of the AlertSystem without the need for actual 
network connections or external dependencies.

Functions:
    test_alert_system_update(monkeypatch): 
        Tests that the AlertSystem's update method prints the correct
        alert message when called with a network status.
"""
from unittest.mock import MagicMock

from observers.alert_system import AlertSystem


def test_alert_system_update(monkeypatch):
    """
    Test that the AlertSystem prints the correct alert message when the update method is called.
    """
    # Create a mock for the print function
    mock_print = MagicMock()
    monkeypatch.setattr("builtins.print", mock_print)

    # Create an instance of AlertSystem and call the update method
    alert_system = AlertSystem()
    test_status = "Connected"
    alert_system.update(test_status)

    # Assert that print was called correctly
    mock_print.assert_called_once_with(
        f"AlertSystem: Alert - Network status is now {test_status}"
    )
