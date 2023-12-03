"""
This module defines the ListFilesCommand class which extends the SSHCommand abstract base class.

The ListFilesCommand class represents the 'ls -l' SSH command for listing files and directories 
on a remote server. It provides an implementation for executing the 'ls -l' command over 
an SSH connection.

Classes:
    ListFilesCommand: Represents the 'ls -l' SSH command for listing files and directories 
    on a remote server.

Attributes:
    ssh_connection (SSHConnection): An instance of the SSH connection over which the 
    command is executed.

Methods:
    __init__(self, ssh_connection): Initializes the ListFilesCommand with an SSH connection.
    execute(self): Executes the 'ls -l' command on the connected remote SSH server.
"""
from commands.ssh_command import SSHCommand


class ListFilesCommand(SSHCommand):
    """
    Represents the 'ls -l' SSH command for listing files and directories on a remote server.

    This class extends the SSHCommand abstract base class, providing an implementation for
    executing the 'ls -l' command. It is used to list files and directories in the current directory
    of the remote server, showcasing detailed information.

    Attributes:
        ssh_connection: An instance of the SSH connection over which the command is executed.

    Methods:
        execute(): Executes the 'ls -l' command on the remote SSH server.
    """

    def __init__(self, ssh_connection):
        """
        Initializes the ListFilesCommand with an SSH connection.

        Args:
            ssh_connection: The SSH connection object used to execute the 'ls -l' command.
        """
        self.ssh_connection = ssh_connection

    def execute(self):
        """
        Executes the 'ls -l' command on the connected remote SSH server.

        Overrides the execute method from the SSHCommand class. It sends the 'ls -l' command
        to the SSH server and returns the output, providing a detailed list of 
        files and directories.

        Returns:
            The output of the 'ls -l' command execution, containing details of files 
            and directories.
        """
        return self.ssh_connection.execute_command("ls -l")
