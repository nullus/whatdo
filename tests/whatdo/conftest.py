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
from unittest.mock import MagicMock

from pytest import fixture

from whatdo.model import Timesheet, Event
from whatdo.port import StorageInterface


@fixture(scope='function')
def storage_adaptor_mock():
    return MagicMock(spec=StorageInterface)


@fixture(scope='function')
def empty_timesheet():
    return Timesheet()


@fixture(scope='function')
def bttf_timesheet():
    timesheet = Timesheet()
    data = [
        (datetime(1955, 11, 5, 6, 15), 'Arrival'),
        (datetime(1955, 11, 12, 22, 4), 'Lightning Strike'),
        (datetime(1985, 10, 26, 1, 20), 'Last Time Departed'),
        (datetime(1985, 10, 26, 1, 21), 'Destination Time'),
        (datetime(1985, 10, 26, 1, 22), 'Present Time'),
        (datetime(1985, 10, 26, 1, 35), 'Escape'),
    ]
    for event in data:
        timesheet.append(Event(*event))
    return timesheet


@fixture(scope='function')
def dup_timesheet():
    timesheet = Timesheet()
    data = [
        (datetime(2018, 9, 2, 15, 0), 'Implement Task grouping'),
        (datetime(2018, 9, 2, 15, 10), 'Implement Task grouping'),
        (datetime(2018, 9, 2, 15, 15), 'Complete Task grouping'),
    ]
    for event in data:
        timesheet.append(Event(*event))
    return timesheet
