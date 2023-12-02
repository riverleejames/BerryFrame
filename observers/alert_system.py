"""
This module defines the AlertSystem class, a concrete implementation of the Observer
design pattern. The AlertSystem class is part of a larger framework that manages
network connections and is used to observe changes in network connection status.

Classes:
    AlertSystem: A subclass of Observer that reacts to network status updates by
                 printing alert messages.

The AlertSystem class is intended to be used within systems that require real-time
monitoring and notification of network status changes. When integrated into a network
connection management system, it can provide immediate feedback, such as printing
messages or triggering alerts, in response to changes in network connectivity.
"""

from model.backend.connection_manager import Observer


class AlertSystem(Observer):
    """
    A concrete observer that prints an alert message upon receiving network status updates.

    The AlertSystem class extends the Observer class and overrides the update method
    to provide a specific reaction to changes in network status. When the update
    method is called, typically by a subject it is observing, the AlertSystem prints
    a message indicating the new network status.

    This class can be used in any system where real-time monitoring and response to
    network status changes are required, such as in server monitoring tools, network
    diagnostic applications, or automated alert systems.

    Methods:
        update(status): Overrides the Observer update method to print an alert message
                        with the current network status.

    Example:
        alert_system = AlertSystem()
        alert_system.update('Connected')
        # Output: AlertSystem: Alert - Network status is now Connected
    """

    def update(self, status):
        """
        Responds to network status updates by printing an alert message.

        This method is called when the subject (typically a network connection manager)
        notifies its observers about a change in network status. The method prints
        a formatted message to indicate the current status of the network.

        Args:
            status (str): The current status of the network connection.

        Examples:
            When the network status changes to 'Connected':
            >>> alert_system = AlertSystem()
            >>> alert_system.update('Connected')
            AlertSystem: Alert - Network status is now Connected
        """
        print(f"AlertSystem: Alert - Network status is now {status}")
