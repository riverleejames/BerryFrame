"""
This module defines a set of API function classes for remote system operations. 

It includes classes for executing remote commands, retrieving system statistics, 
and uploading and downloading files using a connection manager. Each class inherits 
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
        """
        Abstract method to execute an API function.

        This method should be implemented by each subclass of APIFunction. It defines the
        specific operation that the API function will perform. The method can accept a
        variable number of arguments and keyword arguments, allowing flexibility in the
        implementation of the function in each subclass.

        Args:
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.

        Raises:
            NotImplementedError: If this method is not overridden in a subclass.
        """
        raise NotImplementedError("Subclasses should implement this!")


class ExecuteRemoteCommand(APIFunction):
    """
    API function for executing a remote command.

    This class allows the execution of a command on a remote server using the ConnectionManager.
    It handles specific exceptions related to SSH connections and command execution.
    """

    def execute(self, command):
        """
            Executes a specified command on a remote server.

            This method connects to the remote server using the ConnectionManager and executes
            the provided command. It returns the command's output or an error message if an
            exception occurs.

            Args:
                command (str): The command to be executed on the remote server.

            Returns:
                str: The output of the executed command, or an error message if the execution fails.

            Raises:
                SSHException: Raised when there is an issue with the SSH connection.
                AuthenticationException: Raised for authentication issues.
                ConnectionResetError: Raised when the connection is reset unexpectedly.
            """
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
        """
           Retrieves various system statistics from a remote server.

           This method gathers CPU usage, memory usage, disk space, and running process counts
           by executing relevant system commands on the remote server. It utilizes the
           ExecuteRemoteCommand class for executing these commands.

           Returns:
               tuple: A tuple containing CPU usage, memory usage, disk space, and running process count.
           """
        command_executor = ExecuteRemoteCommand()
        cpu_usage = command_executor.execute("top -bn1 | grep 'Cpu(s)' | awk '{print $2+$4}'")
        memory_usage = command_executor.execute(
            "free -m | awk 'NR==2{printf \"Memory Usage: %s/%sMB (%.2f%%)\", $3,$2,$3*100/$2 }'"
        )
        disk_space = command_executor.execute('df -h | awk \'$NF=="/"{printf "Disk Usage: %d/%dGB (%s)", $3,$2,$5}\'')
        running_processes = command_executor.execute("ps -e | wc -l")

        return cpu_usage, memory_usage, disk_space, running_processes


class UploadFile(APIFunction):
    """
    API function for uploading a file.

    This class handles uploading a file from a local path to a remote path. It manages
    the SFTP client provided by the ConnectionManager for file transfer.
    """

    def execute(self, local_path, remote_path):
        """
           Uploads a file from the local system to a remote server.

           This method establishes an SFTP connection via the ConnectionManager and uploads
           a file from the specified local path to the specified remote path.

           Args:
               local_path (str): The path of the file on the local system to be uploaded.
               remote_path (str): The path on the remote server where the file will be stored.

           Raises:
               IOError: Raised if there is an issue with file reading or writing.
               SSHException: Raised if there is an issue with the SFTP connection.
           """
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
        """
            Downloads a file from a remote server to the local system.

            This method establishes an SFTP connection via the ConnectionManager and downloads
            a file from the specified remote path to the specified local path.

            Args:
                remote_path (str): The path of the file on the remote server to be downloaded.
                local_path (str): The path on the local system where the file will be stored.

            Raises:
                IOError: Raised if there is an issue with file reading or writing.
                SSHException: Raised if there is an issue with the SFTP connection.
            """
        connection_manager = ConnectionManager.get_instance()
        sftp_client = connection_manager.ssh_client.open_sftp()
        sftp_client.get(remote_path, local_path)
        sftp_client.close()
