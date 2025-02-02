from abc import ABC, abstractmethod


class BaseGitHubMetric(ABC):
    """
    Abstract base class for GitHub metrics.

    This class serves as the foundation for all GitHub metric implementations.
    It enforces a structure where each metric must implement the `get_data` method
    and provides a standardized response format.

    Attributes:
        order (int): Determines the execution order of metrics. Default is 100.

    Methods:
        get_data(username): Abstract method that must be implemented by subclasses
                            to retrieve specific metric data.
        format_response(key, data): Formats the output response into a dictionary.
    """

    def __init__(self):
        """
        Initializes the base metric with a default order value.

        The `order` attribute can be overridden in subclasses to determine
        the priority in which metrics are executed.
        """
        self.order = 100

    @abstractmethod
    def get_data(self, username):
        """
        Abstract method to be implemented by subclasses.

        Args:
            username (str): The GitHub username for which to retrieve metric data.

        Returns:
            dict: The formatted metric data.
        """
        pass

    @staticmethod
    def format_response(key, data):
        """
        Formats the response data into a standardized dictionary structure.

        Args:
            key (str): The key representing the metric type.
            data (any): The data associated with the metric.

        Returns:
            dict: A dictionary with the metric key mapped to the corresponding data.
        """
        return {key: data}
