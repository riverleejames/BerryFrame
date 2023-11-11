"""
This is the main script for establishing an SSH connection to a server, executing 
a sample command, and then closing the connection. It uses the ConnectionManager 
and api_functions modules to manage the connection and execute commands. The script 
reads configuration settings from a 'config.ini' file.

The script demonstrates how to:
- Read SSH connection details from a configuration file.
- Use the ConnectionManager class to establish and manage an SSH connection.
- Execute a remote command using the execute_remote_command function.
- Disconnect from the SSH server after completing operations.
"""

import configparser
from backend.connection_manager import ConnectionManager
from backend.api_functions import execute_remote_command

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
    CONNECTION_MANAGER.connect(host, port, username, password, key_path)

    # Execute a sample command and print the output
    output = execute_remote_command("ls")
    print(output)

    # Disconnect from the server
    CONNECTION_MANAGER.disconnect()
