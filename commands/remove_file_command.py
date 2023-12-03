"""
This module defines the RemoveFileCommand class which extends the SSHCommand abstract base class.

The RemoveFileCommand class represents a concrete SSH command for removing a file 
on a remote server. It provides an implementation for executing the 'rm' command 
over an SSH connection.

Classes:
    RemoveFileCommand: Represents a concrete SSH command for removing a file on a remote server.

Attributes:
    ssh_connection (SSHConnection): An instance of the SSH connection to execute commands.
    filename (str): The name of the file to be removed.

Methods:
    __init__(self, ssh_connection, filename): Initializes the RemoveFileCommand with 
    the SSH connection and the filename.
    execute(self): Executes the remove file command on the SSH server.
"""
from commands.ssh_command import SSHCommand

class RemoveFileCommand(SSHCommand):
    """
    A concrete SSH command class for removing a file on a remote server.

    This class extends the SSHCommand abstract base class, providing a specific implementation
    of the execute method for removing a file. It encapsulates all the details necessary to
    perform the file removal operation over an established SSH connection.

    Attributes:
        ssh_connection: An instance of the SSH connection to execute commands.
        filename (str): The name of the file to be removed.

    Methods:
        execute(): Executes the command to remove a file on the SSH server.
    """

    def __init__(self, ssh_connection, filename):
        """
        Initializes the RemoveFileCommand with the SSH connection and the filename.

        Args:
            ssh_connection: The SSH connection object to execute the command.
            filename (str): The name of the file to be removed.
        """
        self.ssh_connection = ssh_connection
        self.filename = filename

    def execute(self):
        """
        Executes the remove file command on the SSH server.

        This method overrides the execute method from the SSHCommand class.
        It sends a command to the SSH server to remove the specified file.

        Returns:
            The result of the file removal command execution.
        """
        return self.ssh_connection.execute_command(f'rm {self.filename}')
