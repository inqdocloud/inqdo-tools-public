import io
import sys

from inqdo_tools.utils.logger import SequenceLogger


def test_collect_logs():
    seq_logger = SequenceLogger("Test Logger")
    seq_logger.collect_logs("Log 1", "Value 1")
    seq_logger.collect_logs("Log 2", "Value 2")

    assert len(seq_logger.logs) == 2
    assert seq_logger.logs[0] == ("[1] Log 1", "Value 1")
    assert seq_logger.logs[1] == ("[2] Log 2", "Value 2")


def test_sequence_logger_with_long_name():
    seq_logger = SequenceLogger("Test Logger with a Very Long Name")
    seq_logger.collect_logs("Log 1", "Value 1")

    captured_output = io.StringIO()
    sys.stdout = captured_output

    seq_logger.print_logs()

    assert "==== Test Logger with a Very Long Name ====" in captured_output.getvalue()

    sys.stdout = sys.__stdout__
