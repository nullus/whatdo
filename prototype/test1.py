from __future__ import print_function

import argparse
import datetime
import os


class Activity(object):
    def __init__(self, duration, description):
        self.duration = duration
        self.description = description

    # def __eq__(self, other):
    #     return self.description == other.description

    # def __hash__(self):
    #     return hash(self.description)

    def __str__(self):
        return "{0} {1}".format(str(self.duration), self.description)


class Event(object):
    def __init__(self, timestamp, description):
        self.timestamp = timestamp
        self.description = description

    @classmethod
    def first(class_):
        return class_(datetime.datetime.min, None)

    # @classmethod
    # def last(class_):
    #     return class_(datetime.datetime.max, None)

    def to_activity(self, next_):
        return Activity(next_.timestamp - self.timestamp, self.description)


def timesheet_events(filename='~/timesheet'):
    with open(os.path.expanduser(filename), 'r') as timesheet_file:
        for line in timesheet_file:
            if line.startswith("#"):
                continue
            (timestamp_str, description) = line.split()
            timestamp = datetime.datetime.strptime(timestamp_str, '%Y-%m-%dT%H:%M')
            yield Event(timestamp, description)


def event_activity(events):
    event = Event.first()
    for next_event in events:
        yield event.to_activity(next_event)
        event = next_event


def __main__():
    print(sum([i.duration for i in event_activity(timesheet_events()) if i.description == 'SC2!'], datetime.timedelta()))


if __name__ == "__main__":
    __main__()