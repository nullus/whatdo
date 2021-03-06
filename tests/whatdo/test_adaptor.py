# coding: utf-8
#
# BSD 2-Clause License
#
# Copyright (c) 2018, Dylan Perry <dylan.perry@gmail.com>
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# * Redistributions of source code must retain the above copyright notice,
#   this list of conditions and the following disclaimer.
#
# * Redistributions in binary form must reproduce the above copyright notice,
#   this list of conditions and the following disclaimer in the documentation
#   and/or other materials provided with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.
#
from datetime import datetime, timezone
from unittest.mock import MagicMock, mock_open, patch

from pytest import raises

from whatdo.adaptor import CommandLine, MemoryStorage, CsvStorage
from whatdo.port import Timetracker


def test_command_line_initialise_success():
    """Can initialise CommandLine with Timetracker port"""

    timetracker = MagicMock()
    # noinspection PyTypeChecker
    command_line = CommandLine(timetracker)
    assert isinstance(command_line, CommandLine)


def test_command_line_call_no_arguments_will_exit():
    """Calling CommandLine with an empty arguments list will exit"""

    timetracker = MagicMock()
    with raises(SystemExit):
        # noinspection PyTypeChecker
        command_line = CommandLine(timetracker)
        command_line([])


def test_command_line_call_with_arguments_invokes_log_event():
    """When CommandLine is called with multiple arguments invoke log_event"""

    timetracker = MagicMock()
    # noinspection PyTypeChecker
    command_line = CommandLine(timetracker)
    command_line('many arguments are also accepted'.split(' '))
    timetracker.log_event.assert_called_once()
    timetracker.log_event.assert_called_with('many arguments are also accepted')


def test_command_line_call_with_one_argument_invokes_log_event():
    """When CommandLine is called invoke log_event"""

    timetracker = MagicMock(spec=Timetracker)
    # noinspection PyTypeChecker
    command_line = CommandLine(timetracker)
    command_line(['one'])
    timetracker.log_event.assert_called_once()
    timetracker.log_event.assert_called_with('one')


def test_command_line_call_with_today_argument_produces_summary(capsys):
    timetracker = MagicMock(spec=Timetracker)
    # noinspection PyTypeChecker
    command_line = CommandLine(timetracker)
    timetracker.task_summary_by_day.return_value = [
        (2.0, 'Stuff and things')
    ]
    command_line(['today'])
    (out, _) = capsys.readouterr()
    assert '2h\tStuff and things' in out


def test_memory_storage_initialise_success():
    """Can initialise a MemoryStorage adaptor"""

    memory_storage = MemoryStorage()
    assert isinstance(memory_storage, MemoryStorage)


def test_memory_storage_store_records():
    test_data = [
        (datetime(1985, 10, 26, 1, 21), 'Destination Time'),
        (datetime(1985, 10, 26, 1, 22), 'Present Time'),
        (datetime(1985, 10, 26, 1, 20), 'Last Time Departed'),
    ]

    memory_storage = MemoryStorage()
    memory_storage.store(iter(test_data))


def test_memory_storage_retrieve_records():
    test_data = [
        (datetime(1985, 10, 26, 1, 21), 'Destination Time'),
        (datetime(1985, 10, 26, 1, 22), 'Present Time'),
        (datetime(1985, 10, 26, 1, 20), 'Last Time Departed'),
    ]

    memory_storage = MemoryStorage()
    memory_storage.store(iter(test_data))

    i = 0
    for i, record in enumerate(memory_storage.retrieve()):
        assert record[0] == test_data[i][0]
        assert record[1] == test_data[i][1]

    assert i == len(test_data) - 1


def test_csv_storage_initialise_success():
    csv_storage = CsvStorage()
    assert isinstance(csv_storage, CsvStorage)


def test_csv_storage_store_opens_file():
    test_data = [
        (datetime(1985, 10, 26, 1, 21), 'Destination Time'),
        (datetime(1985, 10, 26, 1, 22), 'Present Time'),
        (datetime(1985, 10, 26, 1, 20), 'Last Time Departed'),
    ]

    csv_storage = CsvStorage()
    with patch('whatdo.adaptor.open', mock_open()) as open_:
        csv_storage.store(test_data)

    open_.assert_called_once_with('timesheet.csv', 'w')


def test_csv_storage_store_writes_record():
    test_data = [(datetime(1985, 10, 26, 1, 21, tzinfo=timezone.utc), 'Destination Time'), ]

    csv_storage = CsvStorage()
    with patch('whatdo.adaptor.open', mock_open()) as open_:
        csv_storage.store(test_data)

    handle = open_()
    handle.write.assert_called_once_with('1985-10-26T01:21:00.000000,Destination Time\r\n')


def test_csv_storage_retrieve_succeeds_with_missing_file():
    csv_storage = CsvStorage()
    with patch('whatdo.adaptor.open') as open_:
        open_.side_effect = FileNotFoundError('Boom')
        list(csv_storage.retrieve())

    open_.assert_called_once_with('timesheet.csv', 'r')


def test_csv_storage_retrieve_opens_file():
    csv_storage = CsvStorage()
    with patch('whatdo.adaptor.open', mock_open()) as open_:
        list(csv_storage.retrieve())

    open_.assert_called_once_with('timesheet.csv', 'r')


def test_csv_storage_retrieve_reads_record():
    csv_data = '1985-10-26T01:21:00.000000,Destination Time\r\n'

    csv_storage = CsvStorage()
    with patch('whatdo.adaptor.open', mock_open(read_data=csv_data)) as open_:
        # Make open_ behave like an iterator
        open_.return_value.__iter__ = lambda self: self
        open_.return_value.__next__ = lambda self: next(iter(self.readline, ''))
        test_data = list(csv_storage.retrieve())

    # We need to make the a non timezone aware datetime for comparison
    assert test_data[0] == (datetime(1985, 10, 26, 1, 21, tzinfo=timezone.utc).astimezone(tz=None).replace(tzinfo=None),
                            'Destination Time')
