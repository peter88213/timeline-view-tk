"""Timeline viewer unit tests.

Copyright (c) 2025 Peter Triesberger
For further information see https://github.com/peter88213/timeline-view-tk
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
import unittest

from tlv_model.tlv_data_model import TlvDataModel
from tlv_model.tlv_section import TlvSection
from tlv_model.tlv_csv_reader import TlvCsvReader

TEST_CSV_FILE = 'data/test_dates.csv'
FAULTY_CSV_FILE = 'data/not_a_timeline.csv'
NONEXISTENT_FILE = 'data/nonexistent.csv'
REFERENCE_DATE = '2024-07-13'
DATA_TABLE = [
    ['ID', 'Title', 'Desc', 'Date', 'Time', 'Day', 'LastsDays', 'LastsHours', 'LastsMinutes'],
    ['sc1', 'TlvSection 5', '', '2024-07-14', '18:56', '', '', '', '20'],
    ['sc2', 'The second event', '', '2024-07-14', '14:15', '', '', '2', ''],
    ['sc3', 'TlvSection 3', '', '2024-07-14', '18:15', '', '', '', '2'],
    ['sc4', 'TlvSection six (no time)', '', '2024-07-14', '', '', '', '', ''],
    ['sc5', 'TlvSection 4', '', '2024-07-14', '18:16', '', '', '', '20'],
    ['sc6', 'TlvSection 1', '', '2024-07-14', '13:00', '', '', '1', '30'],
    ['sc7', 'TlvSection Seven (second day)', '', '', '13:00', '2', '', '1', '30'],
    ['sc8', 'TlvSection Eight (second day, no time)', '', '', '', '2', '', '1', '30'],
    ['sc9', 'TlvSection Nine (time only)', '', '', '18:16', '', '', '1', '30'],
    ['sc10', 'TlvSection Ten (no data)', '', '', '', '', '', '', ''],
    ['', '', '', '2024-07-13', '', '0', '', '', ''],
]
TEST_SECTIONS = dict(
    sc1=TlvSection(
        title='TlvSection 5',
        scDate='2024-07-14',
        scTime='18:56',
        lastsMinutes='20'
        ),
    sc2=TlvSection(
        title='The second event',
        scDate='2024-07-14',
        scTime='14:15',
        lastsHours='2'
        ),
    sc3=TlvSection(
        title='TlvSection 3',
        scDate='2024-07-14',
        scTime='18:15',
        lastsMinutes='2'
        ),
    sc4=TlvSection(
        title='TlvSection six (no time)',
        scDate='2024-07-14',
        ),
    sc5=TlvSection(
        title='TlvSection 4',
        scDate='2024-07-14',
        scTime='18:16',
        lastsMinutes='20'
        ),
    sc6=TlvSection(
        title='TlvSection 1',
        scDate='2024-07-14',
        scTime='13:00',
        lastsHours='1',
        lastsMinutes='30',
        ),
    sc7=TlvSection(
        title='TlvSection Seven (second day)',
        day='2',
        scTime='13:00',
        lastsHours='1',
        lastsMinutes='30',
        ),
    sc8=TlvSection(
        title='TlvSection Eight (second day, no time)',
        day='2',
        lastsHours='1',
        lastsMinutes='30',
        ),
    sc9=TlvSection(
        title='TlvSection Nine (time only)',
        scTime='18:16',
        lastsHours='1',
        lastsMinutes='30',
        ),
    sc10=TlvSection(
        title='TlvSection Ten (no data)',
        ),
)


class TestCsvReader(unittest.TestCase):

    def test_get_data_table(self):
        reader = TlvCsvReader()
        self.assertEqual(reader.get_data_table(TEST_CSV_FILE), DATA_TABLE)


class TestTlvDataModel(unittest.TestCase):

    def test_set_data(self):
        model = TlvDataModel()
        model.set_data(DATA_TABLE)
        for scId in TEST_SECTIONS:
            self.assertEqual(model.sections[scId].title, TEST_SECTIONS[scId].title)
            self.assertEqual(model.sections[scId].desc, TEST_SECTIONS[scId].desc)
            self.assertEqual(model.sections[scId].date, TEST_SECTIONS[scId].date)
            self.assertEqual(model.sections[scId].time, TEST_SECTIONS[scId].time)
            self.assertEqual(model.sections[scId].day, TEST_SECTIONS[scId].day)
            self.assertEqual(model.sections[scId].lastsDays, TEST_SECTIONS[scId].lastsDays)
            self.assertEqual(model.sections[scId].lastsHours, TEST_SECTIONS[scId].lastsHours)
            self.assertEqual(model.sections[scId].lastsMinutes, TEST_SECTIONS[scId].lastsMinutes)
        self.assertEqual(model.referenceDate, REFERENCE_DATE)

    def test_read_data_normal(self):
        model = TlvDataModel()
        model.read_data(TEST_CSV_FILE)
        for scId in TEST_SECTIONS:
            self.assertEqual(model.sections[scId].title, TEST_SECTIONS[scId].title)
            self.assertEqual(model.sections[scId].desc, TEST_SECTIONS[scId].desc)
            self.assertEqual(model.sections[scId].date, TEST_SECTIONS[scId].date)
            self.assertEqual(model.sections[scId].time, TEST_SECTIONS[scId].time)
            self.assertEqual(model.sections[scId].day, TEST_SECTIONS[scId].day)
            self.assertEqual(model.sections[scId].lastsDays, TEST_SECTIONS[scId].lastsDays)
            self.assertEqual(model.sections[scId].lastsHours, TEST_SECTIONS[scId].lastsHours)
            self.assertEqual(model.sections[scId].lastsMinutes, TEST_SECTIONS[scId].lastsMinutes)
        self.assertEqual(model.referenceDate, REFERENCE_DATE)

    def test_read_data_faulty_file(self):
        model = TlvDataModel()

        with self.assertRaises(ValueError) as exc:
            model.read_data(FAULTY_CSV_FILE)
        self.assertEqual(str(exc.exception), f'Wrong data structure in "{FAULTY_CSV_FILE}"')

    def test_read_data_nonexistent_file(self):
        model = TlvDataModel()

        with self.assertRaises(FileNotFoundError) as exc:
            model.read_data(NONEXISTENT_FILE)
        self.assertEqual(str(exc.exception), f"[Errno 2] No such file or directory: '{NONEXISTENT_FILE}'")


if __name__ == "__main__":
    unittest.main()
