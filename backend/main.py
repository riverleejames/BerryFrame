"""
This is the main script for establishing an SSH connection to a server, executing 
a sample command, and then closing the connection. It utilizes the ConnectionManager 
and api_functions modules to manage the connection and execute commands.
"""

from backend.api_functions import execute_remote_command
from backend.connection_manager import ConnectionManager


if __name__ == "__main__":
    CONNECTION_MANAGER = ConnectionManager.get_instance()
    CONNECTION_MANAGER.connect("your_raspberry_pi_ip", "your_username", "your_password")
    output = execute_remote_command("ls")
    print(output)
    CONNECTION_MANAGER.disconnect()
