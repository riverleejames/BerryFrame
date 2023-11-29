"""
This module defines a factory for creating instances of API function classes.

The APIFunctionFactory class in this module is responsible for instantiating
and returning objects of various API function classes such as ExecuteRemoteCommand,
GetSystemStats, UploadFile, and DownloadFile based on the requested function type.
"""

from api.api_functions import (
    DownloadFile,
    ExecuteRemoteCommand,
    GetSystemStats,
    UploadFile,
)


class APIFunctionFactory:
    """
    A factory class for creating API function objects.

    This class provides a method to create instances of different API function classes
    based on the specified function type. It supports creating objects for executing
    remote commands, getting system statistics, uploading files, and downloading files.
    """

    def create_api_function(self, function_type):
        """
        Creates and returns an instance of an API function class.

        Based on the provided function type, this method instantiates and returns
        the corresponding API function class object. If an unknown function type
        is specified, it raises a ValueError.

        Parameters:
            function_type (str): The type of API function to create. Expected values
                                 are "ExecuteRemoteCommand", "GetSystemStats",
                                 "UploadFile", or "DownloadFile".

        Returns:
            An instance of the specified API function class.

        Raises:
            ValueError: If an unknown function type is specified.
        """
        if function_type == "ExecuteRemoteCommand":
            return ExecuteRemoteCommand()
        elif function_type == "GetSystemStats":
            return GetSystemStats()
        elif function_type == "UploadFile":
            return UploadFile()
        elif function_type == "DownloadFile":
            return DownloadFile()
        else:
            raise ValueError(f"Unknown API function type: {function_type}")
