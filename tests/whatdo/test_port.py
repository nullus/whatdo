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

from datetime import datetime

from whatdo.model import Timesheet
from whatdo.port import Storage, Timetracker


def test_create_timetracker():
    """Can create instance of Timetracker"""

    timesheet = Timesheet()
    timetracker = Timetracker(timesheet)
    assert isinstance(timetracker, Timetracker)


def test_timetracker_log_event_succeeds():
    """Record and event using timetracker"""

    timesheet = Timesheet()
    timetracker = Timetracker(timesheet)
    timetracker.log_event("We are doing a thing")
    assert len(timesheet) == 1


def test_create_storage(empty_timesheet, storage_adaptor_mock):
    """Can create Storage instance"""

    storage = Storage(empty_timesheet, storage_adaptor_mock)
    assert isinstance(storage, Storage)


def test_storage_persist_succeeds(empty_timesheet, storage_adaptor_mock):
    """Storage port can persist data"""

    storage = Storage(empty_timesheet, storage_adaptor_mock)
    assert storage.persist()


def test_storage_init_retrieves_records(empty_timesheet, storage_adaptor_mock):
    storage_adaptor_mock.retrieve.return_value = iter([
        (datetime(1985, 10, 26, 1, 21), 'Destination Time'),
        (datetime(1985, 10, 26, 1, 22), 'Present Time'),
        (datetime(1985, 10, 26, 1, 20), 'Last Time Departed'),
    ])
    Storage(empty_timesheet, storage_adaptor_mock)
    assert storage_adaptor_mock.retrieve.called_once()
    assert 3 == len(empty_timesheet)
