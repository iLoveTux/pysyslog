# -*- coding: utf-8 -*-

"""Top-level package for pysyslog."""

__author__ = """Clifford Bressette"""
__email__ = 'cliffbressette@gmail.com'
__version__ = '0.1.0'

from .pysyslog import (
    log_writer,
    ThreadedTCPServer,
    QueuedTCPRequestHandler,
)
