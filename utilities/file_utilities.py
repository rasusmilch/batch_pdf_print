import os
import shutil
from .log_util import *
import hashlib
import fnmatch

def calculate_checksum(file_path, algorithm='md5'):
    """Calculate the checksum of a file."""
    try:
        hash_func = hashlib.new(algorithm)
        with open(file_path, 'rb') as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_func.update(chunk)
        return hash_func.hexdigest()
    except Exception as e:
        log_error(f"Failed to calculate checksum for {file_path}: {e}")
        return None

def should_exclude(path, excluded_patterns):
    """Check if a path should be excluded based on patterns."""
    for pattern in excluded_patterns:
        if fnmatch.fnmatch(path, pattern):
            return True
    return False

def sync_directories(remote_dir, local_dir, excluded_dir_patterns, excluded_file_patterns):
    """Sync files from the remote directory to the local directory, excluding directories and files based on patterns."""
    try:
        for root, dirs, files in os.walk(remote_dir):
            relative_path = os.path.relpath(root, remote_dir)
            
            # Check if the current directory should be excluded
            if should_exclude(relative_path, excluded_dir_patterns):
                logger.info(f"Skipping excluded directory: {relative_path}")
                # Skip this directory and any subdirectories
                dirs[:] = []
                continue
            
            local_root = os.path.join(local_dir, relative_path)
            
            try:
                if not os.path.exists(local_root):
                    os.makedirs(local_root)
            except Exception as e:
                log_error(f"Failed to create directory {local_root}: {e}")
                continue
            
            for file_name in files:
                remote_file = os.path.join(root, file_name)
                local_file = os.path.join(local_root, file_name)
                
                # Check if the current file should be excluded
                if should_exclude(file_name, excluded_file_patterns):
                    logger.info(f"Skipping excluded file: {remote_file}")
                    continue
                
                try:
                    if os.path.exists(local_file):
                        remote_checksum = calculate_checksum(remote_file)
                        local_checksum = calculate_checksum(local_file)
                        
                        if remote_checksum is None or local_checksum is None:
                            logger.warning(f"Skipping file due to checksum error: {remote_file}")
                            continue

                        if remote_checksum != local_checksum:
                            logger.info(f"Updating {local_file}")
                            shutil.copy2(remote_file, local_file)
                    else:
                        logger.info(f"Copying {remote_file} to {local_file}")
                        shutil.copy2(remote_file, local_file)
                except Exception as e:
                    log_error(f"Failed to sync file {remote_file} to {local_file}: {e}")

    except Exception as e:
        log_error(f"Failed to sync files from {remote_dir} to {local_dir}: {e}")
