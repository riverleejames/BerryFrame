"""
Unit tests for the ConnectionLogger class in the observer module.

This module is dedicated to testing the ConnectionLogger class, particularly its update method.
It aims to verify that the ConnectionLogger correctly logs messages about the network connection
status. Mock objects are utilized to simulate the print functionality, enabling the tests to 
verify output without generating actual console output. This approach ensures that the 
ConnectionLogger behaves as expected in scenarios where the network status changes, 
enhancing the reliability and maintainability of the system's logging features.

Functions:
    test_connection_logger_update(monkeypatch): Tests the functionality of the update method in
                                                ConnectionLogger, ensuring it correctly logs the
                                                status change message.
"""
from unittest.mock import MagicMock

from observers.connection_logger import ConnectionLogger


def test_connection_logger_update(monkeypatch):
    """
    Test that the ConnectionLogger prints the correct message when the update method is called.
    """
    # Mock the print function
    mock_print = MagicMock()
    monkeypatch.setattr("builtins.print", mock_print)

    # Create an instance of ConnectionLogger and call the update method
    logger = ConnectionLogger()
    test_status = "Disconnected"
    logger.update(test_status)

    # Assert that print was called with the correct message
    mock_print.assert_called_once_with(
        f"ConnectionLogger: Network status changed to {test_status}"
    )
