"""
    @brief Utility module component containing all the functions for cli based options
    @author oldgod
"""

# standard module imports
from argparse import ArgumentParser

def parse_cli_args() -> dict:
    '''
        @brief function to parse the CLI arguments and return the parsed options
        @author oldgod
    '''
    args = {}
    parser = ArgumentParser()

    # fixme: add the code for optional arguments here

    # required arguments
    parser.add_argument("-m", "--module", help="Specify the submodule [services]", required=True)

    args = parser.parse_args()
    return vars(args)
