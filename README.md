# What Do

## What

Timetracking

## Why

There are existing tools, but I want to build something:

* Designed around a plug-able core (TBD)
* Completely future facing: Only Python ≥ 3.5, type annotation
* With an idiomatic OO class structure, hexagonal architecture (port/adapter)
* Small enough to be achievable
* Genuinely useful (?)

## How

### Install

Perhaps pip install from github? (inside a virtualenv with Python ≥ 3.5 please)

    pip install git+https://github.com/nullus/whatdo.git@0.2.0
    
### Track all the things

    $ whatdo Eat a potato
    $ whatdo Go for a walk
    
### Examine your exciting day

    $ whatdo today
    40m     Eat a potato

## Foreseeably Asked Questions

### Do I need to log at least two things to see a report?

Yes, this is not a stopwatch

### Can I see things I did on other days?

No

### Did I ever finish my walk?

If you can imagine it, it is possible
