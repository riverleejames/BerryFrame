"""
SSH Command Module for BerryFrame Application.

This module provides the abstract base class for implementing the Command Pattern
in the context of SSH operations within the BerryFrame application. The module's primary
focus is to define a standard interface for SSH commands, enabling a flexible and
extensible approach to handling various SSH operations.

Classes:
    SSHCommand: An abstract base class that serves as a blueprint for concrete SSH command classes.

The SSHCommand class is an essential part of the Command Pattern implementation,
allowing the BerryFrame application to dynamically execute different SSH commands based on
the needs of the operation. This approach helps in maintaining a clean separation of concerns
and enhances the modularity of the application.

Example:
    class ListFilesCommand(SSHCommand):
        def execute(self):
            # Implementation for listing files on the SSH server

    class RemoveFileCommand(SSHCommand):
        def execute(self):
            # Implementation for removing a file on the SSH server
"""

from abc import ABC, abstractmethod


class SSHCommand(ABC):
    """
    An abstract base class representing an SSH command.

    This class serves as the foundation for the Command Pattern in the context of SSH operations.
    It defines a common interface for all concrete SSH command classes, ensuring that each command
    class implements the execute method. This structure allows for the dynamic execution of various
    SSH commands and enhances the flexibility and extensibility of command execution.

    Methods:
        execute(): An abstract method that executes the SSH command.
    """

    @abstractmethod
    def execute(self):
        """
        Abstract method to execute the SSH command.

        This method should be implemented by all concrete SSH command classes derived 
        from this class. The implementation would include the specific logic required 
        to execute the corresponding SSH command.

        Returns:
            The result of the SSH command execution, which may vary based on the command's nature.
        """
        raise NotImplementedError
