#!/usr/bin/env python

# standard modules
from logging import info, debug, DEBUG, INFO, error
from os import getcwd, sep
from traceback import format_exc

# custom modules
from utility import parse_cli_args, modules, chk_pyver, run_module, scribe
from model import GeneralConfig

if __name__ == "__main__":
    try:
        fw_config = GeneralConfig()
        fw_config.read_config(config_file_path=f"{getcwd()}{sep}config{sep}tpas.ini")
        scribe.enable_filelogging(bool(int(fw_config.get_config(section_name="framework", option_name="enablefile")))) # type: ignore
        scribe.enable_streamlogging(bool(int(fw_config.get_config(section_name="framework", option_name="enablestream")))) # type: ignore
        scribe.set_log_level(DEBUG if int(fw_config.get_config(section_name="framework", option_name="enabledebug")) == 1 else INFO) # type: ignore
    except Exception as exception:
        print(exception)

    try:
        if int(fw_config.get_config(section_name="framework", option_name="enabledebug")) == 1: #type: ignore
            debug("Logger has been setup in debug mode")
        else:
            info("Logger has been setup in info mode")
        
        info("Parsing the CLI arguments")
        debug(f"Current working directory : {getcwd()}")
        args = parse_cli_args()
        debug(f"CLI arguments parsed : {args}")

        debug("Checking the required python version")
        chk_pyver()

        if args.get("list"):
            info("Showing the list of modules")
            debug(modules)
            print("Modules available")
            count = 1
            for module in modules.keys():
                debug(f"{count}. {module}")
                print(f"{count}. {module}")
                count += 1
        elif args.get("module"):
            info("Starting module")
            debug(f"Module name to be started : {args.get('module')}")

            run_module(module_name=str(args.get("module")), modules=modules)
    except Exception as exc:
        print("Something went wrong, please check the recent log file(dd_mm_yyyy.log) in the logs directory")
        error(format_exc())
