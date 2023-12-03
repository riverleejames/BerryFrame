"""
Class representing the user interface for SSH-related operations.

The SSHView class is a simple yet crucial component of an SSH management system. It provides a
user-friendly interface for displaying messages, particularly those related to SSH operations
such as connection status, errors, and command outputs. This class abstracts the details of user
interaction, allowing other components of the system to communicate with the user without being
concerned about the specifics of the display mechanism.

Methods:
    show_message: Prints a specified message to the standard output.

The show_message method is straightforward in its implementation, using Python's built-in print
function to display messages. This design choice keeps the class simple and versatile, suitable
for various command-line based applications.

Example:
    ssh_view = SSHView()
    ssh_view.show_message("SSH connection established.")

Note:
    While this class currently uses the standard output for displaying messages, 
    it can be extended or modified to support other types of user interfaces, 
    such as graphical interfaces or logging systems, making it adaptable to 
    different application requirements.
"""


class SSHView:
    """
    A class representing the SSH view.

    This class provides methods for displaying messages related to SSH.
    """

    @staticmethod
    def show_message(message):
        """
        Displays the given message.

        Args:
            message (str): The message to be displayed.
        """
        print(message)
