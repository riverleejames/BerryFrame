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
    def update(self, status):
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
        if ConnectionManager._instance is None:
            ConnectionManager._instance = ConnectionManager()
        return ConnectionManager._instance

    def attach(self, observer):
        self._observers.append(observer)

    def detach(self, observer):
        self._observers.remove(observer)

    def notify(self, status):
        for observer in self._observers:
            observer.update(status)

    def connect(self, host, port, username, password, key_path):
        self.ssh_client.connect(
            host, port, username=username, password=password, key_filename=key_path
        )
        self.notify("Connected")

    def disconnect(self):
        self.ssh_client.close()
        self.notify("Disconnected")

    def execute_command(self, command):
        _, stdout, _ = self.ssh_client.exec_command(command)
        return stdout.read().decode()

    @staticmethod
    def reset_instance():
        ConnectionManager._instance = None
