#!/usr/bin/env python

from logging import info, debug, DEBUG

from uvicorn import run as uvrun

# custom module
from utility import parse_cli_args, modules, chk_pyver, run_module, scribe

# fixme: decide whether this function should be present here or should be moved to utility module
def run_service(host: str="", port: int=5000, nworker: int=1):
    '''
        @brief function to start the API servces
        @author oldgod
    '''
    info(f"Staring services on 0.0.0.0:{port}")
    uvrun("services:app", host="0.0.0.0" if len(host) == 0 else host, port=port, workers=nworker)

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
