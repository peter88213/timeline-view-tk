"""Provide a timeline data model class.

Copyright (c) 2025 Peter Triesberger
For further information see https://github.com/peter88213/timeline-view-tk
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
from tlv_model.tlv_csv_reader import TlvCsvReader

from tlv_model.tlv_section import TlvSection
from tlv_model.tlv_constants import COLUMNS, SC_PREFIX


class TlvDataModel:

    def __init__(self):
        self.sections = {}
        self._referenceDate = None

        self._observers = []
        # list of Observer instance references
        self._isModified = False
        # internal modification flag

        self.dataReader = TlvCsvReader()

    @property
    def isModified(self):
        # Boolean -- True if there are unsaved changes.
        return self._isModified

    @isModified.setter
    def isModified(self, setFlag):
        self._isModified = setFlag
        self.notify_observers()

    @property
    def referenceDate(self):
        return self._referenceDate

    @referenceDate.setter
    def referenceDate(self, newVal):
        if self._referenceDate != newVal:
            self._referenceDate = newVal
            self.on_element_change()

    def add_observer(self, client):
        """Add an observer instance reference to the list."""
        if not client in self._observers:
            self._observers.append(client)

    def delete_observer(self, client):
        """Remove an observer instance reference from the list."""
        if client in self._observers:
            self._observers.remove(client)

    def notify_observers(self):
        for client in self._observers:
            client.refresh()

    def on_element_change(self):
        """Callback function that reports changes."""
        self.isModified = True

    def set_data(self, dataTable):
        assert dataTable[0] == COLUMNS
        self.sections = {}
        for row in dataTable:
            scId = row[0]
            if not scId:
                # Row has no ID: might be the reference date.
                if row[5] == '0' and row[3] is not None:
                    self.referenceDate = row[3]
            elif scId.startswith(SC_PREFIX):
                # Strip ID and convert empty strings to None.
                cells = []
                for i, cell in enumerate(row):
                    if i == 0:
                        # skip ID
                        continue

                    if cell:
                        cells.append(cell)
                    else:
                        cells.append(None)

                self.sections[scId] = TlvSection()
                (
                    self.sections[scId].title,
                    self.sections[scId].desc,
                    self.sections[scId].date,
                    self.sections[scId].time,
                    self.sections[scId].day,
                    self.sections[scId].lastsDays,
                    self.sections[scId].lastsHours,
                    self.sections[scId].lastsMinutes,
                ) = cells
                self.sections[scId].on_element_change = self.on_element_change

    def read_data(self, filePath):
        self.set_data(self.dataReader.get_data_table(filePath))

