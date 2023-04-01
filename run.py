#!/usr/bin/env python

from uvicorn import run as uvrun

# custom module
from utility import parse_cli_args

def run_service():
    '''
        @brief function to start the API servces
        @author oldgod
    '''
    uvrun("services:app", host="0.0.0.0", workers=1)

if __name__ == "__main__":
    args = parse_cli_args()
    print(f"CLI Arguments provided : {args}")
    run_service()

