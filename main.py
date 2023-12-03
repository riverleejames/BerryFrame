"""
Main script to use the Command Pattern for managing SSH connections and executing commands.

...

Example Usage:
    This script can be executed directly from the command line after configuring the 'config.ini' file with
    the appropriate SSH connection details. The script will create command objects for specified SSH commands,
    which are then executed via the SSHCommandInvoker.
"""

import configparser
from controllers.ssh_controller import SSHController
from controllers.command_invoker import SSHCommandInvoker
from commands.list_files_command import ListFilesCommand
from commands.neofetch_command import NeofetchCommand

def main():
    """
    Main function to establish an SSH connection and execute commands using the Command Pattern.
    """
    # Read configuration settings
    config = configparser.ConfigParser()
    config.read("config.ini")

    # Retrieve SSH configuration details
    ssh_config = config["SSH"]
    host = ssh_config.get("host")
    port = ssh_config.getint("port", 22)  # Default to port 22 if not specified
    username = ssh_config.get("username")
    password = ssh_config.get("password")
    key_path = ssh_config.get("key_path")

    # Initialize SSH Controller
    controller = SSHController(host, port, username, password, key_path)

    # Initialize Command Invoker
    invoker = SSHCommandInvoker()

    # Connect to the SSH server
    controller.connect()

    # Create and execute a neofetch command
    neofetch_command = NeofetchCommand(controller)
    print(invoker.execute_command(neofetch_command))

    # Example: Create and execute a list files command
    list_files_command = ListFilesCommand(controller)
    print(invoker.execute_command(list_files_command))

    # Disconnect from the server
    controller.disconnect()

if __name__ == "__main__":
    main()
