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

from argparse import ArgumentParser
from datetime import datetime, timezone
from typing import List, Iterator, Tuple

from .port import StorageInterface, Timetracker


class CommandLine(object):
    """
    Log events to timetracker via command line
    """

    def __init__(self, timetracker: Timetracker) -> None:
        self.timetracker = timetracker

    def __call__(self, arguments: List[str]) -> int:
        parser = ArgumentParser(description=self.__doc__)
        parser.add_argument('what', nargs='+')
        what: str = ' '.join(parser.parse_args(arguments).what)
        self.timetracker.log_event(what)
        return 0


class DatetimeConversionMixin(object):
    P_FMT = '%Y-%m-%dT%H:%M:%S.%f'
    ISO_TIMESPEC = 'microseconds'

    def to_datetime(self, in_: str) -> datetime:
        return datetime.strptime(in_, self.P_FMT).replace(tzinfo=timezone.utc).astimezone(tz=None).replace(tzinfo=None)

    def from_datetime(self, out: datetime) -> str:
        return out.astimezone(tz=timezone.utc).replace(tzinfo=None).isoformat(timespec=self.ISO_TIMESPEC)


class MemoryStorage(DatetimeConversionMixin, StorageInterface):
    """
    Back storage interface with list
    """

    def __init__(self) -> None:
        super().__init__()
        self.data: List[Tuple[str, str]] = []

    def retrieve(self) -> Iterator[Tuple[datetime, str]]:
        for record in self.data:
            yield self.to_datetime(record[0]), record[1]

    def store(self, records: Iterator[Tuple[datetime, str]]) -> None:
        self.data.clear()
        for record in records:
            self.data.append((self.from_datetime(record[0]), record[1]))
