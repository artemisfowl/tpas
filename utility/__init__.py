"""
    @brief Default initialization file for utility module
    @author oldgod
"""

# standard module
from os import getcwd

# custom module 
from .cli import parse_cli_args
from .helper import list_submodules, chk_pyver, run_module
from .log import Scribe

scribe = Scribe()
modules = list_submodules(getcwd())
