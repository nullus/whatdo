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

from abc import ABC, abstractmethod
from datetime import datetime

from typing import Iterator, Tuple

from .model import Timesheet, Event


class Timetracker(object):
    def __init__(self, timesheet: Timesheet) -> None:
        super().__init__()
        self.timesheet = timesheet

    def log_event(self, what: str) -> None:
        self.timesheet.append(Event(datetime.now(), what))


class StorageInterface(ABC):
    @abstractmethod
    def store(self, records: Iterator[Tuple[datetime, str]]) -> None:
        pass

    @abstractmethod
    def retrieve(self) -> Iterator[Tuple[datetime, str]]:
        pass


class Storage(object):
    def __init__(self, timesheet: Timesheet, adaptor: StorageInterface) -> None:
        self.timesheet = timesheet
        self.adaptor = adaptor
        self._restore()

    def _restore(self) -> None:
        for record in self.adaptor.retrieve():
            self.timesheet.append(Event(record[0], record[1]))

    def persist(self) -> None:
        self.adaptor.store((record.when, record.what) for record in self.timesheet)
