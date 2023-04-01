#!/usr/bin/env python

# custom module
from utility import parse_cli_args

def run_service():
    '''
        @brief
    '''
    print("Starting services run")

if __name__ == "__main__":
    args = parse_cli_args()
    print(f"CLI Arguments provided : {args}")

