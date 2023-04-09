#!/usr/bin/env python

from logging import DEBUG, error, info, debug

from uvicorn import run as uvrun

# custom module
from utility import parse_cli_args, scribe, modules, chk_pyver

# fixme: decide whether this function should be present here or should be moved to utility module
def run_service(host: str="", port: int=5000, nworker: int=1):
    '''
        @brief function to start the API servces
        @author oldgod
    '''
    info(f"Staring services on 0.0.0.0:{port}")
    uvrun("services:app", host="0.0.0.0" if len(host) == 0 else host, port=port, workers=nworker)

if __name__ == "__main__":
    args = parse_cli_args()
    
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

        if str(args.get("module")).lower() in modules:
            # fixme: add a module switcher in helper file
            pass
        else:
            error(f"Unknown module : {args.get('module')} specified to start")

