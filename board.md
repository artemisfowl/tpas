## To Do

- Add Logger module
    > Add the logger module to enable logging of the various operations performed inside the framework.
    * [x] Add capacity of logging
    * [x] Add capacity for reading the configuration file, the default one for the framework and based on that create the logger instance
    * [x] Add capacity for enabling reload while in debug mode is selected
    * [ ] Add the function for adding separate handlers to the root logger
    * [ ] Add capacity for isolating the log lines in a separate file of choice from user/by test-name

## Doing

- Add Services module
    > Add a services module which will be hosting all the services as well as the background work for Web UI automation.
    * [x] Add all imports to the __init__.py file
    * [x] Add a constants file containing all the necessary constants for the services module
    * [ ] Relocate backend logic to mangler file
    * [ ] Create web driver session based on the configured browser
    * [ ] If no configured browser, create the selenium web driver session for the default browser

## Done

- Add Utility module
    > Add the utility module which will contain certain common routines/sub-routines for use in the TPAS framework.
    * [x] Add proper documentation strings for all the functions till date
    * [x] Add files in Utility module
    * [x] Add the imports in the module __init__ file
    * [x] Add code for reading the configuration file
    * [x] Add code for running a specific module
    * [x] Add constants to be used all throughout the framework
