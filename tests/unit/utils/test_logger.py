import io
import sys
import os

from inqdo_tools.utils.logger import SequenceLogger, InQdoLogger


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


def test_inqdo_logger_with_prefix():
    os.environ["LOG_TEST"] = "true"
    inqdo_logger = InQdoLogger("TEST")
    
    captured_output = io.StringIO()
    sys.stdout = captured_output

    inqdo_logger.print("Test print")
    
    assert "[TEST] - Test print" in captured_output.getvalue()
    assert inqdo_logger.prefix == "TEST"
    
    sys.stdout = sys.__stdout__