"""Provide a class for reading csv data files.

Copyright (c) 2025 Peter Triesberger
For further information see https://github.com/peter88213/timeline-view-tk
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
import csv

from tlv_model.tlv_reader import TlvReader
from tlv_model.tlv_constants import SC_PREFIX
from tlv_model.tlv_section import TlvSection
from tlv_model.id_generator import IdGenerator


class TlvCsvReader(TlvReader):

    COLUMNS = [
        'Title',
        'Desc',
        'Date',
        'Time',
        'Day',
        'LastsDays',
        'LastsHours',
        'LastsMinutes'
    ]

    def read(self, filePath):
        with open(filePath, newline='') as f:
            dataReader = csv.reader(f)
            dataTable = list(dataReader)
        if dataTable[0] != self.COLUMNS:
            raise ValueError(f'Wrong data structure in "{filePath}"')

        self._mdl.sections = {}
        for row in dataTable[1:]:
            scId = IdGenerator.new_id(self._mdl.sections, SC_PREFIX)
            if not row[0]:
                # Row has no title: might be the reference date.
                if row[4] == '0' and row[2] is not None:
                    self._mdl.referenceDate = row[2]
                continue

            cells = []
            for cell in row:
                if cell:
                    cells.append(cell)
                else:
                    cells.append(None)

            self._mdl.sections[scId] = TlvSection()
            (
                self._mdl.sections[scId].title,
                self._mdl.sections[scId].desc,
                self._mdl.sections[scId].date,
                self._mdl.sections[scId].time,
                self._mdl.sections[scId].day,
                self._mdl.sections[scId].lastsDays,
                self._mdl.sections[scId].lastsHours,
                self._mdl.sections[scId].lastsMinutes,
            ) = cells
            self._mdl.sections[scId].on_element_change = self._mdl.on_element_change

