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

from whatdo.model import Event, Timesheet, Task, TaskSummary


def test_event_created():
    """Create an event"""

    event = Event(datetime.now(), 'Something happened')
    assert isinstance(event, Event)


def test_event_properties_match():
    """Event properties are equal to parameters"""

    when = datetime(1985, 10, 26, 1, 22)
    what = 'Something happened'
    event = Event(when, what)
    assert when == event.when
    assert what == event.what


def test_timesheet_append_event_succeeds(empty_timesheet):
    """Can append an event to a timesheet"""

    empty_timesheet.append(Event(datetime.now(), 'Something happened'))
    assert 1 == len(empty_timesheet)


def test_timesheet_append_other_fails():
    """Can't append other types to a timesheet"""

    timesheet = Timesheet()
    with raises(TypeError):
        # noinspection PyTypeChecker
        timesheet.append("Boom")


def test_empty_timesheet_find_returns_empty_timesheet(empty_timesheet):
    events = empty_timesheet.find(datetime(1985, 10, 26), datetime(1985, 10, 27))

    assert 0 == len(events)


def test_bttf_timesheet_find_start_returns_partial_timesheet(bttf_timesheet):
    events = bttf_timesheet.find(start=datetime(1985, 10, 26, 1, 21))

    assert 3 == len(events)


def test_bttf_timesheet_find_end_returns_partial_timesheet(bttf_timesheet):
    events = bttf_timesheet.find(end=datetime(1985, 10, 26, 1, 21))

    assert 3 == len(events)


def test_bttf_timesheet_find_none_returns_equivalent_timesheet(bttf_timesheet):
    events = bttf_timesheet.find()

    assert bttf_timesheet == events


def test_timesheet_to_tasks_gives_task_list(empty_timesheet):
    # For an arbitrary value of now
    empty_timesheet.append(Event(datetime(2018, 8, 31, 18, 50), 'Now'))
    # If I'm not typing that quickly
    empty_timesheet.append(Event(datetime(2018, 8, 31, 18, 51), 'Also now'))

    tasks = empty_timesheet.to_tasks()
    assert 1 == len(tasks)


def test_timesheet_to_tasks_gives_valid_task(bttf_timesheet):
    tasks = bttf_timesheet.to_tasks()
    assert timedelta(days=7, hours=15, minutes=49) == tasks[0].duration
    assert 'Arrival' == tasks[0].what


def test_timesheet_to_tasks_gives_all_tasks(bttf_timesheet):
    tasks = bttf_timesheet.to_tasks()
    assert timedelta(minutes=13) == tasks[4].duration
    assert 'Present Time' == tasks[4].what


@mark.skip('WIP')
def test_timesheet_to_tasks_groups_by_what(dup_timesheet):
    tasks = dup_timesheet.to_tasks()
    assert 1 == len(tasks)


def test_task_created():
    task = Task(timedelta(hours=1), 'Something happened')
    assert isinstance(task, Task)


def test_task_add_task_with_same_what_adds_duration():
    task = Task(timedelta(hours=1), 'This') + Task(timedelta(hours=5), 'This')
    assert Task(timedelta(hours=6), 'This') == task
    assert timedelta(hours=6) == task.duration


def test_task_add_task_with_different_what_raises_value_error():
    with raises(ValueError):
        Task(timedelta(hours=1), 'This') + Task(timedelta(hours=5), 'That')


def test_task_summary_created():
    task_summary = TaskSummary([Task(timedelta(hours=1), 'Refactoring')])
    assert isinstance(task_summary, TaskSummary)


def test_task_summary_summarise_tasks():
    task_summary = TaskSummary([
        Task(timedelta(hours=1), 'Refactoring'),
        Task(timedelta(hours=2), 'Refactoring'),
    ])
    assert 1 == len(task_summary)


def test_task_summary_summarise_duration():
    task_summary = TaskSummary([
        Task(timedelta(hours=1), 'Refactoring'),
        Task(timedelta(hours=2), 'Refactoring'),
    ])
    assert Task(timedelta(hours=3), 'Refactoring') == task_summary[0]
    assert timedelta(hours=3) == task_summary[0].duration
