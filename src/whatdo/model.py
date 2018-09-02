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
from collections import OrderedDict
from datetime import datetime, timedelta
from typing import List, Optional, Iterable, Dict


class Task(object):
    def __init__(self, duration: timedelta, what: str) -> None:
        self.duration = duration
        self.what = what


class Event(object):
    """
    An event, timestamp and generic description
    """

    def __init__(self, when: datetime, what: str) -> None:
        super().__init__()
        self.when = when
        self.what = what

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Event):
            return False
        return self.when == other.when and self.what == other.what

    def to_task(self, end: 'Event') -> Task:
        return Task(end.when - self.when, self.what)


class TaskSummary(OrderedDict, Dict[str, timedelta]):
    def __init__(self, tasks: Iterable[Task]) -> None:
        super().__init__()
        for task in tasks:
            self[task.what] += task.duration

    def __missing__(self, key: str) -> timedelta:
        self[key] = value = timedelta()
        return value


class Timesheet(List[Event]):
    """
    Collection of events
    """

    def append(self, item: Event) -> None:
        if not isinstance(item, Event):
            raise TypeError(f"Expected item to be Event (got {type(item)})")
        return super().append(item)

    def find(self, start: datetime = datetime.min, end: datetime = datetime.max) -> 'Timesheet':
        return Timesheet([event for event in self if start <= event.when < end])

    def to_tasks(self) -> List[Task]:
        return [x.to_task(y) for x, y in zip(self, self[1:])]
