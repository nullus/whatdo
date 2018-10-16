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

from datetime import datetime, date

from behave import *

from whatdo.entry import Cli
from whatdo.adaptor import MemoryStorage


@given("a new instance of whatdo command line")
def step_impl(context):
    context.instance = Cli(storage_interface=MemoryStorage)
    # FIXME: internal knowledge?
    assert 0 == len(context.instance.storage_interface)


@when('we invoke whatdo with argument "{what}"')
def step_impl(context, what):
    context.instance.run([what])


@then("whatdo will record a new event")
def step_impl(context):
    # FIXME: internal knowledge?
    assert 1 == len(context.instance.storage_interface)


@given("a log containing events")
def step_impl(context):
    context.instance.storage_interface.store(
        (datetime.combine(date.today(), datetime.strptime(row["When"], "%H:%M").time()), row["What"])
        for row in context.table
    )
    assert 3 == len(context.instance.storage_interface)


@then("whatdo will report")
def step_impl(context):
    # Rewind capture object
    context.stdout_capture.seek(0)
    # Force encoding on text to permit use of escape characters
    assert context.text.encode('ascii').decode('unicode_escape') in ''.join(context.stdout_capture.readlines())
