"""
This module provides functions to execute various remote commands on a server 
using an SSH connection managed by the ConnectionManager. It includes utilities 
for fetching system statistics like CPU usage, memory usage, disk space, and 
running processes.
"""

from paramiko import SSHException, AuthenticationException
from backend.connection_manager import ConnectionManager


def execute_remote_command(command):
    """
    Executes a given command on the remote server using an established SSH connection.

    Args:
        command (str): The command to be executed on the remote server.

    Returns:
        str: The output of the executed command, or an error message in case of failure.
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


def get_system_stats():
    """
    Retrieves various system statistics such as CPU usage, memory usage,
    disk space, and running processes from a Raspberry Pi.

    Returns:
        Tuple[str, str, str, str]: A tuple containing CPU usage, memory usage,
                                   disk space, and list of running processes.
    """
    cpu_usage = execute_remote_command("top -bn1 | grep 'Cpu(s)' | awk '{print $2+$4}'")
    memory_usage = execute_remote_command(
        "free -m | awk 'NR==2{printf \"Memory Usage: %s/%sMB (%.2f%%)\", $3,$2,$3*100/$2 }'"
    )
    disk_space = execute_remote_command(
        'df -h | awk \'$NF=="/"{printf "Disk Usage: %d/%dGB (%s)", $3,$2,$5}\''
    )
    running_processes = execute_remote_command("ps -e | wc -l")

    return cpu_usage, memory_usage, disk_space, running_processes


def upload_file(local_path, remote_path):
    """
    Uploads a file from the local system to the remote server.

    This function establishes an SFTP client through the current SSH connection
    and uses it to transfer a file from the local system to the specified path
    on the remote server.

    Args:
        local_path (str): The path of the file on the local system.
        remote_path (str): The target path on the remote server where the file will be uploaded.

    Note:
        The function assumes an active SSH connection managed by ConnectionManager.
    """
    connection_manager = ConnectionManager.get_instance()
    sftp_client = connection_manager.ssh_client.open_sftp()
    sftp_client.put(local_path, remote_path)
    sftp_client.close()


def download_file(remote_path, local_path):
    """
    Downloads a file from the remote server to the local system.

    This function sets up an SFTP client using the existing SSH connection
    to retrieve a file from the remote server and save it at the specified
    path on the local system.

    Args:
        remote_path (str): The path of the file on the remote server.
        local_path (str): The target path on the local system where the file will be saved.

    Note:
        An active SSH connection managed by ConnectionManager is required for this function to work.
    """
    connection_manager = ConnectionManager.get_instance()
    sftp_client = connection_manager.ssh_client.open_sftp()
    sftp_client.get(remote_path, local_path)
    sftp_client.close()
