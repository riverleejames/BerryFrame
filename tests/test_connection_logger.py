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
