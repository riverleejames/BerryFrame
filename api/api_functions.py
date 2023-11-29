"""
This module defines a set of API function classes for remote system operations. 

It includes classes for executing remote commands, retrieving system statistics, 
uploading and downloading files using a connection manager. Each class inherits 
from the base class 'APIFunction' and implements an execute method for its specific functionality.
"""

from paramiko import SSHException, AuthenticationException
from backend.connection_manager import ConnectionManager


class APIFunction:
    """
    Base class for API functions.

    This class serves as a template for all API functions, requiring subclasses
    to implement the execute method.
    """

    def execute(self, *args, **kwargs):
        raise NotImplementedError("Subclasses should implement this!")


class ExecuteRemoteCommand(APIFunction):
    """
    API function for executing a remote command.

    This class allows execution of a command on a remote server using the ConnectionManager.
    It handles specific exceptions related to SSH connections and command execution.
    """

    def execute(self, command):
        try:
            # Get the singleton instance of ConnectionManager
            connection_manager = ConnectionManager.get_instance()
            # Execute the command and get the output
            output = connection_manager.execute_command(command)
            # Trim the output to remove unnecessary whitespaces and newlines
            return output.strip()
        except (SSHException, AuthenticationException, ConnectionResetError) as e:
            # Handle specific exceptions (e.g., connection issues, command errors)
            return f"Error executing command '{command}': {e}"


class GetSystemStats(APIFunction):
    """
    API function for retrieving system statistics.

    Retrieves statistics such as CPU usage, memory usage, disk space, and running processes
    on a remote system. It utilizes the ExecuteRemoteCommand class for executing system commands.
    """

    def execute(self):
        command_executor = ExecuteRemoteCommand()
        cpu_usage = command_executor.execute(
            "top -bn1 | grep 'Cpu(s)' | awk '{print $2+$4}'"
        )
        memory_usage = command_executor.execute(
            "free -m | awk 'NR==2{printf \"Memory Usage: %s/%sMB (%.2f%%)\", $3,$2,$3*100/$2 }'"
        )
        disk_space = command_executor.execute(
            'df -h | awk \'$NF=="/"{printf "Disk Usage: %d/%dGB (%s)", $3,$2,$5}\''
        )
        running_processes = command_executor.execute("ps -e | wc -l")

        return cpu_usage, memory_usage, disk_space, running_processes


class UploadFile(APIFunction):
    """
    API function for uploading a file.

    This class handles uploading a file from a local path to a remote path. It manages
    the SFTP client provided by the ConnectionManager for file transfer.
    """

    def execute(self, local_path, remote_path):
        connection_manager = ConnectionManager.get_instance()
        sftp_client = connection_manager.ssh_client.open_sftp()
        sftp_client.put(local_path, remote_path)
        sftp_client.close()


class DownloadFile(APIFunction):
    """
    API function for downloading a file.

    This class handles downloading a file from a remote path to a local path. It manages
    the SFTP client provided by the ConnectionManager for file transfer.
    """

    def execute(self, remote_path, local_path):
        connection_manager = ConnectionManager.get_instance()
        sftp_client = connection_manager.ssh_client.open_sftp()
        sftp_client.get(remote_path, local_path)
        sftp_client.close()
