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

from unittest.mock import MagicMock

from pytest import raises

from whatdo.adaptor import CommandLine


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

    timetracker = MagicMock()
    # noinspection PyTypeChecker
    command_line = CommandLine(timetracker)
    command_line(['one'])
    timetracker.log_event.assert_called_once()
    timetracker.log_event.assert_called_with('one')
