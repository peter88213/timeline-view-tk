"""Provide an abstract base class for data file readers.

Copyright (c) 2025 Peter Triesberger
For further information see https://github.com/peter88213/timeline-view-tk
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
from abc import ABC
from abc import abstractmethod


class TlvReader(ABC):

    @abstractmethod
    def get_data_table(self, filePath):
        pass

