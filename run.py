#!/usr/bin/env python

# custom module
from utility import parse_cli_args

# fixme: add argument parser for parsing the cli [utility module]

def run_service():
    print("Starting services run")
    pass

if __name__ == "__main__":
    args = parse_cli_args()
    print(f"CLI Arguments provided : {args}")

