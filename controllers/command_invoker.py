"""
SSH Command Invoker Module for BerryFrame Application.

This module defines the SSHCommandInvoker class, an integral component of the BerryFrame 
application's Command Pattern implementation. SSHCommandInvoker is responsible for executing 
SSH command objects and maintaining a history of these executions. This functionality allows 
for a flexible and extensible approach to managing and tracking SSH command execution within
the application.

The SSHCommandInvoker class acts as an invoker in the Command Pattern, providing a method to 
execute various SSH commands while keeping a record of their execution. This record is useful 
for auditing, debugging, and reviewing the history of SSH operations performed.

Classes:
    SSHCommandInvoker: Executes SSH command objects and maintains a history of these executions.

Key Features:
    - Executes SSH command objects using a standard interface.
    - Maintains a history of executed commands and their results for tracking and auditing purposes.
    - Demonstrates the use of the Command Pattern in executing and managing SSH operations.
    - Enhances the flexibility and modularity of the SSH command execution process.
"""


class SSHCommandInvoker:
    """
    A class responsible for invoking SSH commands and maintaining a history of executed commands.

    This class serves as an invoker in the Command Pattern, executing command objects
    and keeping track of command execution history. It allows for a flexible and extensible
    approach to executing different types of SSH commands.

    Attributes:
        history (list): A list to store the history of executed commands and their results.

    Methods:
        execute_command(command): Executes a given SSH command and stores it in the history.
        show_history(): Prints the history of executed commands and their results.
    """

    def __init__(self):
        """
        Initializes the SSHCommandInvoker with an empty history list.
        """
        self.history = []

    def execute_command(self, command):
        """
        Executes the given SSH command and appends it to the command history.

        Args:
            command (SSHCommand): The SSH command object to be executed.

        Returns:
            The result of the executed command.

        Note:
            The command object should implement an execute method.
        """
        result = command.execute()
        self.history.append((command, result))
        return result

    def show_history(self):
        """
        Displays the history of executed commands along with their results.

        This method iterates through the command history, printing the details
        of each executed command and its corresponding result.
        """
        for command, result in self.history:
            print(f"Executed: {command} with result: {result}")
