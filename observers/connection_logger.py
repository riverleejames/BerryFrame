"""
This module contains the ConnectionLogger class, a specialized implementation of 
the Observer design pattern. It is part of a network connection management system 
and is responsible for logging changes in the network connection status.

Classes:
    ConnectionLogger: A subclass of Observer that logs network status updates.

The ConnectionLogger class is particularly useful in scenarios where monitoring 
and logging of network connection statuses are essential. This could include 
applications in network management, diagnostics, or any system where keeping 
track of network status changes is critical for operation or troubleshooting.
"""

from backend.connection_manager import Observer


class ConnectionLogger(Observer):
    """
    A concrete observer for logging network status changes in a connection management system.

    The ConnectionLogger class inherits from the Observer interface and implements
    the update method. This method is invoked in response to changes in the network
    status, typically notified by a subject such as a connection manager. Upon
    receiving the update, ConnectionLogger logs the new network status.

    This class is ideal for use in systems that require logging of network status
    changes for monitoring or diagnostic purposes.

    Methods:
        update(status): Overrides the Observer update method to log the network status.

    Example:
        connection_logger = ConnectionLogger()
        connection_logger.update('Disconnected')
        # Output: ConnectionLogger: Network status changed to Disconnected
    """

    def update(self, status):
        """
        Logs a message indicating a change in the network status.

        This method is called when the observed subject (like a network connection manager)
        notifies its observers of a status change. It prints a formatted message to
        log the current network status.

        Args:
            status (str): The updated status of the network connection.

        Examples:
            When the network status changes to 'Disconnected':
            >>> connection_logger = ConnectionLogger()
            >>> connection_logger.update('Disconnected')
            ConnectionLogger: Network status changed to Disconnected
        """
        print(f"ConnectionLogger: Network status changed to {status}")
