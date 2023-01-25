import os


def newline_logger(value, prefix=False):
    v = value
    if prefix:
        v = f"[{prefix}] - {value}"

    print("\n")
    print("===================")
    print(v)
    print("===================")
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
