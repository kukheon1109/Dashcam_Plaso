# -*- coding: utf-8 -*-
"""The Google Chrome Cache files event formatter."""

from __future__ import unicode_literals

from plaso.formatters import interface
from plaso.formatters import manager


class DashcamEventFormatter(interface.ConditionalEventFormatter):
  """Formatter for a Chrome Cache entry event."""

  DATA_TYPE = 'dashcam:metadata'

  FORMAT_STRING_PIECES = [
      '{data_flag}',
    ':',
    '{original_data}'
  ]

  SOURCE_LONG = 'Dashcam MetaData'
  SOURCE_SHORT = 'METADATA'


manager.FormattersManager.RegisterFormatter(DashcamEventFormatter)
