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


from datetime import datetime, timedelta

from pytest import raises, mark

from whatdo.model import Event, Timesheet, Task


def test_event_created():
    """Create an event"""

    event = Event(datetime.now(), 'Something happened')
    assert isinstance(event, Event)


def test_event_properties_match():
    """Event properties are equal to parameters"""

    when = datetime(1985, 10, 26, 1, 22)
    what = 'Something happened'
    event = Event(when, what)
    assert event.when == when
    assert event.what == what


def test_timesheet_append_event_succeeds(empty_timesheet):
    """Can append an event to a timesheet"""

    empty_timesheet.append(Event(datetime.now(), 'Something happened'))
    assert len(empty_timesheet) == 1


def test_timesheet_append_other_fails():
    """Can't append other types to a timesheet"""

    timesheet = Timesheet()
    with raises(TypeError):
        # noinspection PyTypeChecker
        timesheet.append("Boom")


def test_empty_timesheet_find_returns_empty_array(empty_timesheet):
    events = empty_timesheet.find(datetime(1985, 10, 26), datetime(1985, 10, 27))

    assert len(events) == 0


def test_bttf_timesheet_find_start_returns_partial_array(bttf_timesheet):
    events = bttf_timesheet.find(start=datetime(1985, 10, 26, 1, 21))

    assert len(events) == 3


def test_bttf_timesheet_find_end_returns_partial_array(bttf_timesheet):
    events = bttf_timesheet.find(end=datetime(1985, 10, 26, 1, 21))

    assert len(events) == 3


def test_bttf_timesheet_find_none_returns_equivalent_array(bttf_timesheet):
    events = bttf_timesheet.find()

    assert events == bttf_timesheet


def test_task_created():
    task = Task(timedelta(hours=1), 'Something happened')
    assert isinstance(task, Task)
