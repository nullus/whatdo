
Feature: Log event
    So that timesheets can be filled with minimal effort
    As a command line user
    I want to be able to log events with a simple command

  Scenario: Log an event now via command line
      Given a new instance of whatdo command line
      When we invoke whatdo with argument "Hello there"
      Then whatdo will record a new event
