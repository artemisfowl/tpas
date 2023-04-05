'''
    @brief Utility module component containing all the functions for cli based options
    @author oldgod
'''

# standard module imports
from argparse import ArgumentParser

def parse_cli_args() -> dict:
    '''
        @brief function to parse the CLI arguments and return the parsed options
        @author oldgod
    '''
    args = {}
    parser = ArgumentParser(description="Program to run Testing Platform As Service(TPAS)")

    # optional arguments

    # required arguments
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("-m", "--module", help="Specify the submodule [services]", required=False, action="store", nargs=1)
    group.add_argument("-l", "--list", help="Show the list of available modules", required=False, action="store_true")

    args = parser.parse_args()
    return vars(args)
