import os
import sys
from .logging import *
import shutil
from .messagebox import *

def check_and_update_module(module_name, network_module_path):
    """
    Check if the module on the network drive is newer than the local cached copy.
    If it is, copy the module over and reload it.

    :param network_module_path: The path to the module on the network drive.
    :param module_name: The name of the module to check and update.
    :return: None
    """
    local_cache_dir = os.getcwd()

    try:
        module_file_name = f"{module_name}.py"
        local_module_path = os.path.join(local_cache_dir, module_file_name)

        if os.path.exists(local_module_path):
            network_mod_time = os.path.getmtime(network_module_path)
            local_mod_time = os.path.getmtime(local_module_path)

            if network_mod_time > local_mod_time:
                logger.info(f"Newer version of {module_file_name} found on network. Updating...")
                shutil.copy2(network_module_path, local_module_path)
                logger.info(f"Copied {module_file_name} from network to local cache.")
                MsgBox("Restart Required", "A module was updated, please restart the program", MB_ICONSTOP | MB_OK)
                sys.exit(0)
            else:
                logger.info(f"Local version of {module_file_name} is up to date.")
        else:
            logger.info(f"Local version of {module_file_name} not found. Copying from network...")
            shutil.copy2(network_module_path, local_module_path)
            logger.info(f"Copied {module_file_name} from network to local cache.")
            MsgBox("Restart Required", "A module was updated, please restart the program", MB_ICONSTOP | MB_OK)
            sys.exit(0)

    except FileNotFoundError as e:
        log_error(f"File not found: {e}")
    except PermissionError as e:
        log_error(f"Permission denied: {e}")
    except Exception as e:
        log_error(f"An unexpected error occurred: {e}")