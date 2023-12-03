"""
A concrete SSH command class for executing the Neofetch command on a remote server.
"""
from commands.ssh_command import SSHCommand


class NeofetchCommand(SSHCommand):
    """

    This class extends the SSHCommand abstract base class, providing a specific implementation
    of the execute method for the Neofetch command. Neofetch is a command-line system information
    tool that displays system information in a visually appealing format. This class encapsulates
    the necessary logic to execute the Neofetch command over an established SSH connection.

    Attributes:
        ssh_connection: An instance of the SSH connection to execute commands.

    Methods:
        execute(): Executes the Neofetch command on the SSH server.
    """

    def __init__(self, ssh_connection):
        """
        Initializes the NeofetchCommand with the SSH connection.

        Args:
            ssh_connection: The SSH connection object to execute the Neofetch command.
        """
        self.ssh_connection = ssh_connection

    def execute(self):
        """
        Executes the Neofetch command on the SSH server.

        This method overrides the execute method from the SSHCommand class.
        It sends the Neofetch command to the SSH server and returns its output.

        Returns:
            The output of the Neofetch command execution.
        """
        return self.ssh_connection.execute_command("neofetch")
