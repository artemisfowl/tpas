#!/usr/bin/env python

# standard modules
from logging import info, debug, DEBUG
from os import makedirs
makedirs("./logs", exist_ok=True)

# custom modules
from utility import parse_cli_args, modules, chk_pyver, run_module, scribe

# fixme: change the module file to a module.ini file providing users the capacity to change how the module should be started
# fixme: add the code for creating the log directory at the start of the program

if __name__ == "__main__":
    # enable debug mode for now explicitly
    # fixme: add the configurability to change the logging feature from a configuration file
    scribe.set_log_level(DEBUG)
    
    info("Parsing the CLI arguments")
    args = parse_cli_args()
    debug(f"CLI arguments parsed : {args}")

    debug("Checking the required python version")
    chk_pyver()

    if args.get("list"):
        info("Showing the list of modules")
        print("Modules available")
        count = 1
        for module in modules:
            debug(f"{count}. {module}")
            print(f"{count}. {module}")
            count += 1
    elif args.get("module"):
        info("Starting module")
        debug(f"Module name to be started : {args.get('module')}")

        run_module(module_name=str(args.get("module")), modules=modules)
