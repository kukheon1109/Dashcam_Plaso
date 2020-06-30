# -*- coding: utf-8 -*-
"""The NMEA GPRMC parser plugin interface."""

from __future__ import unicode_literals

from plaso.parsers import logger
from plaso.parsers import plugins

class NMEAPlugin(plugins.BasePlugin):
    """multimedia_dashcam parser plugin."""

    NAME = 'dashcam_metadata'
    DESCRIPTION = 'Parser for DashCam Multimeda files.'

    META_LIST = 'any'

    GPRMC_KEY = frozenset(['GPRMC'])

    def __init__(self):
        super(NMEAPlugin, self).__init__()
        self._gprmcdata = None


    def Process(self, parser_mediator, start_data):
        if start_data is None or start_data != 'GPRMC':
            raise ValueError('It is not NMEA data.')

        super(NMEAPlugin, self).Process(parser_mediator, start_data)



