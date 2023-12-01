"""
Module for managing SSH connections and executing remote commands.

This module contains classes and functions for establishing SSH connections, managing these connections,
and executing commands on a remote server. It follows the Observer pattern to provide updates on connection status.

Classes:
    ConnectionStatusLogger: An observer class that logs connection status changes.
    ConnectionAlertSystem: An observer class that alerts on connection status changes.
    SSHController: Main class to handle SSH connections and command execution.

The SSHController class is central to the module, providing methods to connect to a remote server, execute commands,
and disconnect. It uses the ConnectionManager singleton from the 'backend.connection_manager' module for managing
connections and the APIFunctionFactory from the 'api.api_function_factory' module to execute remote commands.
The SSHView class from the 'views.ssh_view' module is optionally used for displaying messages.

Each method in the SSHController class is designed for a specific operation:
- __init__: Initializes the SSH connection details and observers.
- connect: Establishes a connection with the remote server.
- execute_command: Executes a specified command on the remote server.
- disconnect: Terminates the connection with the remote server.

The module demonstrates the use of design patterns like Singleton (ConnectionManager) and Observer (ConnectionStatusLogger,
ConnectionAlertSystem) to create a robust and maintainable SSH connection handling system.

Example:
    ssh_controller = SSHController(host, port, username, password, key_path)
    ssh_controller.connect()
    ssh_controller.execute_command('ls -l')
    ssh_controller.disconnect()

"""

from backend.connection_manager import ConnectionManager, Observer
from api.api_function_factory import APIFunctionFactory
from views.ssh_view import SSHView


class ConnectionStatusLogger(Observer):
    def update(self, status):
        print(f"[Logger] SSH Connection status changed: {status}")


class ConnectionAlertSystem(Observer):
    def update(self, status):
        print(f"[Alert] Attention: SSH Connection is now {status}")


class SSHController:
    """
    SSHController class handles the SSH connection and execution of remote commands.

    Args:
        host (str): The hostname or IP address of the remote server.
        port (int): The port number for the SSH connection.
        username (str): The username for authentication.
        password (str): The password for authentication.
        key_path (str): The path to the private key file for authentication.
        view (SSHView, optional): The view object for displaying messages. Defaults to None.

    Attributes:
        connection_manager (ConnectionManager): The connection manager instance.
        view (SSHView): The view object for displaying messages.
        host (str): The hostname or IP address of the remote server.
        port (int): The port number for the SSH connection.
        username (str): The username for authentication.
        password (str): The password for authentication.
        key_path (str): The path to the private key file for authentication.
    """

    def __init__(self, host, port, username, password, key_path, view=None):
        self.connection_manager = ConnectionManager.get_instance()
        self.view = view if view is not None else SSHView()
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.key_path = key_path

        # Create and attach observers
        logger = ConnectionStatusLogger()
        alert_system = ConnectionAlertSystem()
        self.connection_manager.attach(logger)
        self.connection_manager.attach(alert_system)

    def connect(self):
        """
        Connects to the remote server using SSH.

        Raises:
            ConnectionError: If the connection fails.

        Returns:
            None
        """
        self.connection_manager.connect(
            self.host, self.port, self.username, self.password, self.key_path
        )
        self.view.show_message("Connected to " + self.host)

    def execute_command(self, command):
        """
        Executes a remote command on the connected server.

        Args:
            command (str): The command to be executed.

        Returns:
            None
        """
        factory = APIFunctionFactory()
        execute_command_function = factory.create_api_function("ExecuteRemoteCommand")
        result = execute_command_function.execute(command)
        self.view.show_message(result)

    def disconnect(self):
        """
        Disconnects from the remote server.

        Returns:
            None
        """
        self.connection_manager.disconnect()
        self.view.show_message("Disconnected")
