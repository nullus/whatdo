Feature: Track time
    So that timesheets can be filled with minimal effort
    As a command line user
    I want to be able to track time with simple commands

    Scenario: Log an event now via command line
        Given a new instance of whatdo command line
        When we invoke whatdo with argument "Hello there"
        Then whatdo will record a new event

    Scenario: Report time spent
        Given a new instance of whatdo command line
        And a log containing events
            | When  | What   |
            | 20:26 | Stuff  |
            | 21:26 | Things |
            | 23:56 | Stop   |
        When we invoke whatdo with argument "today"
        Then whatdo will report
            """
            1h\tStuff
            2h 30m\tThings
            """
