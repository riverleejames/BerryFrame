"""
This module defines the ExecuteRemoteCommand class which extends the SSHCommand abstract base class.

The ExecuteRemoteCommand class represents a command to execute a remote command over SSH. 
It provides an implementation for executing the command over an SSH connection.

Classes:
    ExecuteRemoteCommand: Represents a command to execute a remote command over SSH.

Attributes:
    remote_command (str): The remote command to be executed.

Methods:
    __init__(self, remote_command): Initializes an instance of ExecuteRemoteCommand.
    execute(self): Executes the remote command and returns the result.
"""

from commands.ssh_command import SSHCommand
from model.api.api_function_factory import APIFunctionFactory


class ExecuteRemoteCommand(SSHCommand):
    """
    Represents a command to execute a remote command over SSH.
    """

    def __init__(self, remote_command):
        """
        Initializes an instance of ExecuteRemoteCommand.

        Args:
            remote_command (str): The remote command to be executed.
        """
        self.remote_command = remote_command

    def execute(self):
        """
        Executes the remote command and returns the result.

        Returns:
            str: The result of executing the remote command.
        """
        api_function = APIFunctionFactory.create_api_function("ExecuteRemoteCommand")
        return api_function.execute(self.remote_command)
