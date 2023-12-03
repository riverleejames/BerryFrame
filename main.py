"""
SSH Management System

This module provides an interactive interface for managing SSH connections and executing 
commands on a remote server. It allows users to connect to SSH, execute various commands,
and manage the SSH connection.
"""

import configparser
import sys
from rich.console import Console
from rich.table import Table
from rich.prompt import Prompt

from controllers.ssh_controller import SSHController
from controllers.command_invoker import SSHCommandInvoker
from commands.list_files_command import ListFilesCommand
from commands.neofetch_command import NeofetchCommand
from commands.execute_remote_command import ExecuteRemoteCommand

# Constants
BOLD_YELLOW = "bold yellow"
BOLD_GREEN = "bold green"
BOLD_BLUE = "bold blue"
BOLD_CYAN = "bold cyan"
BOLD_RED = "bold red"
BOLD_MAGENTA = "bold magenta"

console = Console()


def main_menu():
    """
    Displays the main menu for the SSH Management System.

    This function presents a table of options to the user, including connecting to SSH, 
    executing commands, and exiting the program.
    """
    table = Table(
        title="SSH Management System", show_header=False, title_style=BOLD_MAGENTA
    )

    table.add_row("1. Connect to SSH")
    table.add_row("2. Execute Remote Command")
    table.add_row("3. Execute Neofetch Command")
    table.add_row("4. Execute List Files Command")
    table.add_row("5. Disconnect SSH")
    table.add_row("6. Exit")

    console.print(table)


def connect_ssh(controller):
    """
    Connects to an SSH server.

    This function initiates an SSH connection using the provided controller. 
    It displays status messages during the connection process.

    Args:
        controller (SSHController): The controller used to manage SSH connections.
    """
    console.print("Connecting to SSH...", style=BOLD_GREEN)
    controller.connect()
    console.print("Connected.", style=BOLD_BLUE)


def check_ssh_connection(controller):
    """
    Checks and handles the SSH connection status.

    Verifies if an SSH connection is active. If not, it prompts the user to establish a connection.

    Args:
        controller (SSHController): The controller used to check the SSH connection.

    Returns:
        bool: True if SSH is connected or the user opts to connect, False otherwise.
    """
    if not controller.is_connected():
        console.print(
            "SSH is not connected. Would you like to connect now? (yes/no)",
            style=BOLD_YELLOW,
        )
        choice = Prompt.ask("")
        if choice.lower() == "yes":
            connect_ssh(controller)
            return True
        return False
    return True


def execute_neofetch_command(controller, invoker):
    """
    Executes the Neofetch command on the remote server.

    Before executing, it checks if the SSH connection is active. 
    If so, it proceeds to execute the Neofetch command.

    Args:
        controller (SSHController): The controller managing SSH connections.
        invoker (SSHCommandInvoker): The invoker to execute the command.
    """
    if check_ssh_connection(controller):
        console.print("Executing Neofetch Command...", style="bold yellow")
        result = invoker.execute_command(NeofetchCommand(controller))
        console.print(result, style=BOLD_CYAN)


def execute_list_files_command(controller, invoker):
    """
    Executes the command to list files on the remote server.

    This function first checks if the SSH connection is active. 
    If so, it proceeds to execute the command to list files.

    Args:
        controller (SSHController): The controller managing SSH connections.
        invoker (SSHCommandInvoker): The invoker to execute the command.
    """
    if check_ssh_connection(controller):
        console.print("Executing List Files Command...", style=BOLD_YELLOW)
        result = invoker.execute_command(ListFilesCommand(controller))
        console.print(result, style=BOLD_CYAN)


def execute_remote_command(controller, invoker, command):
    """
    Executes a specified remote command on the SSH server.

    This function checks for an active SSH connection before executing the given command.

    Args:
        controller (SSHController): The controller for SSH connections.
        invoker (SSHCommandInvoker): The invoker to execute the command.
        command (str): The command to be executed on the remote server.
    """
    if check_ssh_connection(controller):
        console.print("Executing Remote Command...", style=BOLD_YELLOW)
        result = invoker.execute_command(ExecuteRemoteCommand(command))
        console.print(result, style=BOLD_CYAN)


def disconnect_ssh(controller):
    """
    Disconnects from the SSH server.

    This function safely terminates the SSH connection and displays a status message.

    Args:
        controller (SSHController): The controller managing the SSH connection.
    """
    console.print("Disconnecting from SSH...", style=BOLD_GREEN)
    controller.disconnect()
    console.print("Disconnected.", style=BOLD_BLUE)


def main():
    """
    Main function to run the SSH Management System.

    This function sets up the SSH connection configuration, 
    initializes controllers and invokes, and provides a loop 
    for user interaction with the system's menu.
    """
    config = configparser.ConfigParser()
    config.read("config.ini")

    ssh_config = config["SSH"]
    host = ssh_config.get("host")
    port = ssh_config.getint("port", 22)
    username = ssh_config.get("username")
    password = ssh_config.get("password")
    key_path = ssh_config.get("key_path")

    controller = SSHController(host, port, username, password, key_path)
    invoker = SSHCommandInvoker()

    while True:
        main_menu()
        choice = Prompt.ask(
            "Enter your choice", choices=["1", "2", "3", "4", "5", "6"], default="1"
        )

        if choice == "1":
            connect_ssh(controller)
        elif choice == "2":
            command = Prompt.ask("Enter the command to execute")
            execute_remote_command(controller, invoker, command)
        elif choice == "3":
            execute_neofetch_command(controller, invoker)
        elif choice == "4":
            execute_list_files_command(controller, invoker)
        elif choice == "5":
            disconnect_ssh(controller)
        elif choice == "6":
            console.print("Exiting the program.", style=BOLD_RED)
            if controller.is_connected():
                disconnect_ssh(controller)
            sys.exit()
        else:
            console.print("Invalid choice, please try again.", style=BOLD_RED)


if __name__ == "__main__":
    main()
