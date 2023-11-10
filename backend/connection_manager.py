"""
This module defines the ConnectionManager class, which manages SSH connections 
using the Paramiko library. It is implemented as a singleton to ensure only one 
SSH connection is active at a time. The class provides methods to establish, 
execute commands over, and close SSH connections.
"""


import paramiko


class ConnectionManager:
    """
    A singleton class that manages SSH connections using the `paramiko` library.

    This class is designed as a singleton to ensure that only one instance is used
    throughout the application, providing a centralized point for SSH connection management.
    It initializes an SSH client and sets a policy to automatically add the host key
    if it's missing.

    Attributes:
        ssh_client (paramiko.SSHClient): The SSH client used for connections.

    Methods:
        get_instance(): Returns the singleton instance of the ConnectionManager.
        connect(host, username, password): Establishes an SSH connection to a specified host.
        disconnect(): Closes the SSH connection.
        execute_command(command): Executes a given command on the connected host.
    """

    _instance = None

    def __init__(self):
        """
        Initializes the ConnectionManager instance as a singleton.

        This method sets up the SSH client and configures it to automatically add
        missing host keys. If an instance already exists, it raises a RuntimeError
        to prevent multiple instantiations.

        Raises:
            RuntimeError: If an instance of ConnectionManager already exists.
        """
        if ConnectionManager._instance is not None:
            raise RuntimeError("Singleton class, use get_instance() method")
        self.ssh_client = paramiko.SSHClient()
        self.ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    @staticmethod
    def get_instance():
        """
        Returns the singleton instance of the ConnectionManager.

        If the instance does not exist, it creates and returns a new instance.
        Otherwise, it returns the existing instance.

        Returns:
            ConnectionManager: The singleton instance of the ConnectionManager.
        """
        if ConnectionManager._instance is None:
            ConnectionManager._instance = ConnectionManager()
        return ConnectionManager._instance

    def connect(self, host, username, password):
        """
        Establishes an SSH connection to a specified host.

        Connects using the provided host, username, and password. If the connection
        is successful, the method sets up the SSH client with the given credentials.

        Args:
            host (str): The hostname or IP address of the server to connect to.
            username (str): The username for the SSH connection.
            password (str): The password for the SSH connection.
        """
        self.ssh_client.connect(host, username=username, password=password)

    def disconnect(self):
        """
        Closes the active SSH connection.

        This method shuts down the SSH client and ensures the connection is cleanly closed.
        """
        self.ssh_client.close()

    def execute_command(self, command):
        """
        Executes a command on the connected SSH server and returns the output.

        This method sends a command to the SSH server, waits for the execution to complete,
        and then returns the output as a string.

        Args:
            command (str): The command to execute on the SSH server.

        Returns:
            str: The output from the executed command.
        """
        _, stdout, _ = self.ssh_client.exec_command(command)
        return stdout.read().decode()
