"""
This is the main script for establishing an SSH connection to a server, executing 
a sample command, and then closing the connection. It uses the ConnectionManager 
and api_functions modules to manage the connection and execute commands. The script 
reads configuration settings from a 'config.ini' file and uses the Observer pattern 
to notify components about the SSH connection status.

The script demonstrates how to:
- Read SSH connection details from a configuration file.
- Use the ConnectionManager class to establish and manage an SSH connection.
- Attach observers to the ConnectionManager to react to connection status changes.
- Execute a remote command using the execute_remote_command function.
- Disconnect from the SSH server after completing operations.
"""

import configparser
from api.api_function_factory import APIFunctionFactory
from backend.connection_manager import ConnectionManager, Observer


# Define concrete observer classes
class ConnectionStatusLogger(Observer):
    def update(self, status):
        print(f"[Logger] SSH Connection status changed: {status}")


class ConnectionAlertSystem(Observer):
    def update(self, status):
        print(f"[Alert] Attention: SSH Connection is now {status}")


# Read configuration settings
config = configparser.ConfigParser()
config.read("config.ini")

if __name__ == "__main__":
    # Retrieve SSH configuration details
    ssh_config = config["SSH"]
    host = ssh_config.get("host")
    port = ssh_config.getint("port", 22)  # Default to port 22 if not specified
    username = ssh_config.get("username")
    password = ssh_config.get("password")
    key_path = ssh_config.get("key_path")

    # Establish SSH connection
    CONNECTION_MANAGER = ConnectionManager.get_instance()

    # Create and attach observers
    logger = ConnectionStatusLogger()
    alert_system = ConnectionAlertSystem()
    CONNECTION_MANAGER.attach(logger)
    CONNECTION_MANAGER.attach(alert_system)

    # Connect to the SSH server
    CONNECTION_MANAGER.connect(host, port, username, password, key_path)

    # Execute a sample command and print the output
    factory = APIFunctionFactory()
    execute_command_function = factory.create_api_function("ExecuteRemoteCommand")
    result = execute_command_function.execute("neofetch")
    print(result)

    # Disconnect from the server
    CONNECTION_MANAGER.disconnect()
