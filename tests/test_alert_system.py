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
