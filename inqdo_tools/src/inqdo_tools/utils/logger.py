import os
from typing import Any, List, Tuple, Union


def newline_logger(value, prefix=False):
    v = value
    if prefix:
        v = f"[{prefix}] - {value}"

    seperator = "=" * len(v)

    print("\n")
    print(seperator)
    print(v)
    print(seperator)
    print("\n")


class InQdoLogger(object):
    """
    The InQdoLogger class is used to log values when the logger is enabled.

    It takes in a prefix argument, which is used to indicate the logger and checks
    if the environment variable LOG_prefix is set to true, if so it enables the logger.

    It has a print method which takes in a value argument which is logged if the logger is enabled.

    :param prefix: A string that indicates the logger.
    :type prefix: str
    """

    def __init__(self, prefix):
        self.prefix = prefix
        self.enable_log = False

        self._find_prefix_in_env()

    def _find_prefix_in_env(self):
        for var in os.environ:
            if var == f"LOG_{self.prefix}" and os.environ[var] == "true":
                self.enable_log = True

    def print(self, value):
        if self.enable_log:
            newline_logger(value=value, prefix=self.prefix)


class SequenceLogger(object):
    """
    A class for logging sequences of events or values.

    :param name: A string that indicates the loggers name.
    :type name: str

    Attributes:
        logs (List[Tuple[str, Any]]): The list of logs stored as (prefix, value) pairs.
        sequence_counter (int): The counter for the sequence number of each log.

    Methods:
        collect_log(prefix: str, value: Any): Adds a log to the logs list with the given prefix and value.
        print_logs(): Prints all logs in a formatted manner with a header and footer.
    """

    def __init__(self, name):
        """
        Initializes a new instance of the SequenceLogger class.

        :param name: A string that indicates the loggers name.
        :type name: str
        """
        self.name = name
        self.logs = []
        self.sequence_counter = 1

    def collect_log(self, prefix: str, value: Any):
        """
        Adds a log to the logs list with the given prefix and value.

        :param prefix: The prefix of the log.
        :type prefix: str

        :param value: The value of the log.
        :type value: str
        """
        self.logs.append(self._format(
            counter=self.sequence_counter,
            prefix=prefix,
            value=value
        ))
        self.sequence_counter += 1

    def collect_batch(self, batch_list: List[Tuple[str, str]]):
        for item in batch_list:
            prefix, value = item

            self.logs.append(self._format(
                counter=self.sequence_counter,
                prefix=prefix,
                value=value
            ))

            self.sequence_counter += 1

    def print_logs(self):
        """
        Prints all logs in a formatted manner with a header and footer based on the sequence name.
        """
        longest_string = 10
        margin = 2
        seperator = "=" * int(longest_string / 2 + margin)
        end = "=" * len(self.name)

        print(f"{seperator} {self.name} {seperator}")
        for log in self.logs:
            prefix, value = log
            newline_logger(value, prefix)

        print(f"{seperator}{end}{seperator}")

    @staticmethod
    def _format(counter: str, prefix: str, value: str) -> Tuple[str, str]:
        return (f"[{counter}] {prefix}", value)


class SaveSequenceLogger(object):
    """
    A class that allows for a separate SequenceLogger instance to be passed in
    and have its collect_log method called if the instance is not None.
    """
    def __init__(self, sequence_logger: Union[SequenceLogger, None]):
        """
        :param sequence_logger: An instance of the SequenceLogger class.
        :type sequence_logger: SequenceLogger
        """
        self.sequence_logger = sequence_logger

    def collect_log(self, prefix: str, value: Any):
        """
        Calls the collect_log method of the sequence_logger instance with the given prefix and value, if the
        sequence_logger instance is not None.

        :param prefix: The prefix of the log.
        :type prefix: str

        :param value: The value of the log.
        :type value: str
        """
        if self.sequence_logger:
            self.sequence_logger.collect_log(prefix=prefix, value=value)
