"""
Module for testing the SSHView's show_message method.

This module provides a test case for validating the functionality of the show_message method of the SSHView class.
The test ensures that the show_message method correctly prints the intended message to the standard output.
The SSHView class is part of a system designed to handle SSH connections, and this specific method is responsible
for displaying messages to the user.

The test employs the unittest.mock.patch function to redirect the standard output to a StringIO object, which allows
 for capturing and inspecting the output generated by the show_message method. This approach ensures that the method's
 functionality can be tested in isolation, without the need for actual console output.

Function:
    test_ssh_view_show_message: Tests that the show_message method of SSHView correctly prints a given message.

The test follows these steps:
- It creates an instance of SSHView.
- It redirects the standard output (stdout) to a StringIO object.
- It calls the show_message method of the SSHView instance with a predefined test message.
- It captures the output printed to the redirected stdout.
- It asserts that the captured output matches the expected test message.

This module is essential for ensuring that the SSHView's user feedback mechanism functions correctly, which is crucial
for a system where user interaction and feedback are key components.

Example Usage:
    To run this test, use a testing framework like pytest. Place this test module in the same directory as your tests,
    and run `pytest` in the command line.

"""


from io import StringIO
from unittest.mock import patch

from views.ssh_view import SSHView


def test_ssh_view_show_message():
    """
    Test that the SSHView's show_message method prints the correct message.

    This test case creates an instance of SSHView, redirects the stdout to a StringIO object,
    and calls the show_message method with a test message. It then asserts that the printed
    output matches the test message.
    """
    # Create an instance of SSHView
    ssh_view = SSHView()

    # Redirect stdout to a StringIO object
    output = StringIO()
    with patch("sys.stdout", new=output):
        # Call the show_message method with a test message
        test_message = "Test message"
        ssh_view.show_message(test_message)

    # Get the printed output
    printed_output = output.getvalue().strip()

    # Assert that the printed output matches the test message
    assert printed_output == test_message
