"""Provide a class for reading csv data files.

Copyright (c) 2025 Peter Triesberger
For further information see https://github.com/peter88213/timeline-view-tk
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
import csv

from tlv_model.tlv_reader import TlvReader
from tlv_model.tlv_constants import COLUMNS


class TlvCsvReader(TlvReader):

    def get_data_table(self, filePath):
        with open(filePath, newline='') as csvfile:
            dataReader = csv.reader(csvfile)
            dataTable = list(dataReader)
        if dataTable[0] != COLUMNS:
            raise ValueError(f'Wrong data structure in "{filePath}"')

        return dataTable

