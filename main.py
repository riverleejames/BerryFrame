"""
Main script for managing SSH connections and executing commands on a remote server.

This script illustrates the process of setting up an SSH connection, executing a command,
and then closing the connection. It leverages the SSHController class from the 'controllers.ssh_controller' module
for efficient SSH connection management. The script is configured to read SSH connection details from a 'config.ini'
file and implements the Observer pattern to provide updates on the status of the SSH connection.

Key functionalities demonstrated in this script:
- Reading SSH configuration details from a 'config.ini' file.
- Utilizing the SSHController class for establishing and managing SSH connections.
- Executing a remote command on the server using the execute_command method of SSHController.
- Safely disconnecting from the SSH server after executing the necessary commands.

This script is an example of how to integrate different components (SSHController, configuration file,
and Observer pattern) to create a cohesive and functional SSH management system. It is particularly
useful for scenarios where automated remote server management and command execution are required.

Example Usage:
    This script can be executed directly from the command line after configuring the 'config.ini' file with
    the appropriate SSH connection details. The script will read these details, connect to the specified
    SSH server, execute a predefined command (in this case, 'neofetch'), and then close the connection.

"""

import configparser

from controllers.ssh_controller import SSHController


def main():
    """
    Main function to establish an SSH connection and execute a sample command.
    """
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

        # Initialize SSH Controller
        controller = SSHController(host, port, username, password, key_path)

        # Connect to the SSH server
        controller.connect()

        # Execute a sample command and print the output
        controller.execute_command("neofetch")

        # Disconnect from the server
        controller.disconnect()


if __name__ == "__main__":
    main()
