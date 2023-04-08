#!/usr/bin/env python

from logging import DEBUG, info, debug

from uvicorn import run as uvrun

# custom module
from utility import parse_cli_args, list_submodules, scribe

# fixme: decide whether this function should be present here or should be moved to utility module
def run_service(host: str="", port: int=5000, nworker: int=1):
    '''
        @brief function to start the API servces
        @author oldgod
    '''
    uvrun("services:app", host="0.0.0.0" if len(host) == 0 else host, port=port, workers=nworker)

if __name__ == "__main__":
    args = parse_cli_args()
    
    # at runtime change the log level of the logging functionality
    scribe.set_log_level(log_level=DEBUG)

    if args.get("list"):
        info("Showing the list of modules")
        print("Modules available")
        count = 1
        for module in list_submodules(dir="./"):
            debug(f"{count}. {module}")
            print(f"{count}. {module}")
            count += 1
    elif args.get("module"):
        info("Starting services module")
        run_service()
