"""
    @brief Default initialization file for utility module
    @author oldgod
"""

# custom module 
from .cli import parse_cli_args
from .helper import list_submodules, chk_pyver, run_module
from .log import Scribe

# testme: hopefully this should enable the loggging support by default
scribe = Scribe()
modules = set(list_submodules("./"))
