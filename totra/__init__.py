# -*- coding: utf-8 -*-
import logging

from .version import __version__
from .core import TTrackerSession, how_much_hours, report_activities
from .main import main
from totra.output_format import format_activities, save_output

logging.getLogger(__name__).addHandler(logging.NullHandler())

