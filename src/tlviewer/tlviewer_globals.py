"""Global consants for the timeline viewer application.

Copyright (c) 2025 Peter Triesberger
For further information see https://github.com/peter88213/timeline-view-tk
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
from pathlib import Path

from tlv.tlv_locale import _

prefs = {}
HELP_URL = _('https://peter88213.github.io/timeline-view-tk/help/')
HOME_URL = 'https://github.com/peter88213/timeline-view-tk/'

HOME_DIR = str(Path.home()).replace('\\', '/')
INSTALL_DIR = f'{HOME_DIR}/.tlviewer'
