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

import sys
from typing import Type, List

from .model import Timesheet
from .adaptor import CommandLine, CsvStorage
from .port import Timetracker, StorageInterface, Storage


class Cli(object):
    def __init__(self, storage_interface: Type[StorageInterface] = CsvStorage,
                 timesheet: Type[Timesheet] = Timesheet, timetracker: Type[Timetracker] = Timetracker,
                 command_line: Type[CommandLine] = CommandLine, storage: Type[Storage] = Storage) -> None:
        self.timesheet = timesheet()
        self.storage_interface = storage_interface()
        self.timetracker = timetracker(self.timesheet)
        self.command_line = command_line(self.timetracker)
        self.storage = storage(self.timesheet, self.storage_interface)

    def run(self, args: List[str]) -> int:
        result: int = self.command_line(args)
        self.storage.persist()
        return result


def cli() -> None:
    """Command line entry point for CommandLine adaptor"""

    sys.exit(Cli().run(sys.argv[1:]))
