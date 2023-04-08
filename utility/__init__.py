"""
    @brief Default initialization file for utility module
    @author oldgod
"""

# custom module 
from .cli import parse_cli_args
from .helper import list_submodules
from .log import Scribe

# testme: hopefully this should enable the loggging support by default
scribe = Scribe()
