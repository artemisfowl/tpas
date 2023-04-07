#!/usr/bin/env python

from uvicorn import run as uvrun

# custom module
from utility import parse_cli_args, list_submodules

# fixme: decide whether this function should be present here or should be moved to utility module
def run_service(host: str="", port: int=5000, nworker: int=1):
    '''
        @brief function to start the API servces
        @author oldgod
    '''
    uvrun("services:app", host="0.0.0.0" if len(host) == 0 else host, port=port, workers=nworker)

if __name__ == "__main__":
    args = parse_cli_args()
    print(args)

    # fixme: set up the logging facility.

    if args.get("list"):
        print("Modules available")
        count = 1
        for module in list_submodules(dir="./"):
            print(f"{count}. {module}")
            count += 1
    elif args.get("module"):
        run_service()
