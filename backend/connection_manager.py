"""
This module defines the ConnectionManager class, which manages SSH connections 
using the Paramiko library. Implemented as a singleton, it ensures only one 
SSH connection is active at a time. The class provides methods to establish, 
execute commands over, and close SSH connections.

Additionally, the ConnectionManager class acts as a subject in an Observer pattern, 
notifying registered observers about changes in the connection status. This feature 
enables other components of the system to react appropriately to events like 
establishing or closing an SSH connection.

Classes:
    ConnectionManager: Manages SSH connections and notifies observers about 
                       connection status changes.
    Observer: Abstract class for observers that can be notified by the ConnectionManager.

The ConnectionManager class initializes an SSH client with a policy to automatically 
add missing host keys. It provides functionality to connect to and disconnect from 
an SSH server, execute commands, and manage observers that need to be notified 
of connection status changes.

Usage:
    The ConnectionManager is intended to be used as a singleton to ensure a single 
    point of SSH connection management throughout the application. It can be used 
    to establish a connection, execute commands over SSH, and close the connection. 
    Additionally, other components can register as observers to receive updates 
    on the connection status.
"""

import paramiko


class Observer:
    """
        An abstract class that serves as a template for creating observers in the Observer pattern.

        This class defines the basic structure of an observer that can be attached to the
        ConnectionManager. The observers are intended to react to notifications about
        changes in connection status sent by the ConnectionManager.

        Subclasses should implement the update method to define specific reactions to
        the notifications.

        Methods:
            update(status): An abstract method to be implemented by subclasses for responding
                            to connection status updates.
        """

    def update(self, status):
        """
        Abstract method to be overridden by subclasses to respond to connection status updates.

        This method should be implemented in subclasses to define how the observer
        reacts to changes in connection status. The ConnectionManager calls this method
        with the new connection status as an argument.

        Args:
            status (str): The new connection status. Typically, this would be a string like
                          "Connected" or "Disconnected", indicating the current state of the
                          SSH connection.
        """
        pass


class ConnectionManager:
    """
    A singleton class that manages SSH connections using the `paramiko` library.

    This class is designed as a singleton to ensure that only one instance is used
    throughout the application, providing a centralized point for SSH connection management.
    It initializes an SSH client and sets a policy to automatically add the host key
    if it's missing. It also acts as a subject in the Observer pattern, notifying
    observers about connection status changes.

    Attributes:
        ssh_client (paramiko.SSHClient): The SSH client is used for connections.
        _observers (list): List of observers to be notified of connection status changes.

    Methods:
        get_instance(): Returns the singleton instance of the ConnectionManager.
        connect(host, port, username, password, key_path): Establishes an SSH connection to host.
        disconnect(): Closes the SSH connection.
        execute_command(command): Executes a given command on the connected host.
        attach(observer): Attaches an observer.
        detach(observer): Detaches an observer.
        notify(status): Notifies all observers of the connection status.
    """

    _instance = None

    def __init__(self):
        if ConnectionManager._instance is not None:
            raise RuntimeError("Singleton class, use get_instance() method")
        self.ssh_client = paramiko.SSHClient()
        self.ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self._observers = []

    @staticmethod
    def get_instance():
        """
                Retrieves the singleton instance of the ConnectionManager.

                This method ensures that only one instance of ConnectionManager is created and used
                throughout the application, adhering to the singleton design pattern.

                Returns:
                    ConnectionManager: The singleton instance of the ConnectionManager.
                """
        if ConnectionManager._instance is None:
            ConnectionManager._instance = ConnectionManager()
        return ConnectionManager._instance

    def attach(self, observer):
        """
               Attaches an observer to the ConnectionManager.

               This method allows an observer to be added to the internal list, enabling it to receive
               notifications about connection status changes.

               Args:
                   observer (Observer): The observer that will be notified of connection status changes.
               """
        self._observers.append(observer)

    def detach(self, observer):
        """
               Detaches an observer from the ConnectionManager.

               This method removes an observer from the internal list, stopping it from receiving
               further notifications about connection status changes.

               Args:
                   observer (Observer): The observer to be removed.
               """
        self._observers.remove(observer)

    def notify(self, status):
        """
               Notifies all attached observers of a change in connection status.

               This method is called internally whenever there is a change in the connection status,
               such as after connecting or disconnecting from the SSH server.

               Args:
                   status (str): The connection status to be notified to the observers.
               """
        for observer in self._observers:
            observer.update(status)

    def connect(self, host, port, username, password, key_path):
        """
               Establishes an SSH connection to a specified host.

               This method sets up an SSH connection using the provided credentials. It also notifies
               the observers about the connection status.

               Args:
                   host (str): The hostname or IP address of the SSH server.
                   port (int): The port number of the SSH server.
                   username (str): The username for SSH authentication.
                   password (str): The password for SSH authentication.
                   key_path (str): The file path to the SSH private key.

               Raises:
                   SSHException: If the connection fails or other SSH-related errors occur.
               """
        self.ssh_client.connect(host, port, username=username, password=password, key_filename=key_path)
        self.notify("Connected")

    def disconnect(self):
        """
               Closes the active SSH connection.

               This method disconnects from the SSH server and notifies observers about the
               disconnection status.
               """
        self.ssh_client.close()
        self.notify("Disconnected")

    def execute_command(self, command):
        """
               Executes a given command on the connected SSH host.

               This method sends a command to the SSH server and returns its output.

               Args:
                   command (str): The command to execute on the SSH server.

               Returns:
                   str: The output returned from executing the command on the server.

               Raises:
                   SSHException: If the command execution fails or other SSH-related errors occur.
               """
        _, stdout, _ = self.ssh_client.exec_command(command)
        return stdout.read().decode()

    @staticmethod
    def reset_instance():
        """
               Resets the singleton instance of the ConnectionManager.

               This method is used to reset the instance of the ConnectionManager, primarily
               for testing or re-initialization purposes.
               """
        ConnectionManager._instance = None
