import json
import os
from pathlib import Path


def list_to_string(print_list: list) -> str:
    """Converts a list into a newline-separated string, for easy output printing.

    Args:
        print_list (list)

    Returns:
        str: Converted string of list contents, separated by line.
    """
    return '\n'.join([str(item) for item in print_list])


class Dict(dict):
    """dot.notation access to dictionary attributes"""
    __getattr__ = dict.__getitem__
    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__


class Config(object):
    """A class to load and parse data from JSON configuration files."""
    
    @staticmethod
    def __load__(data):
        if type(data) is dict:
            return Config.load_dict(data)
        elif type(data) is list:
            return Config.load_list(data)
        else:
            return data
    
    @staticmethod
    def load_dict(data: dict):
        result = Dict()
        for k, v in data.items():
            result[k] = Config.__load__(v)
        return result
    
    @staticmethod
    def load_list(data: list):
        result = [Config.__load__(item) for item in data]
        return result
    
    @staticmethod
    def load_json(path: str):
        with open(path, "r") as f:
            result = Config.__load__(json.loads(f.read()))
        return result


def get_subdirectories(path: str, just_names: bool = False) -> list:
    """Returns a list of all subdirectories in `path`.

    Args:
        path (str): The root directory that will be scanned.
        just_names (bool, optional): If True, **only** return the NAMES of subdirectories! Defaults to False.

    Returns:
        list: All paths/names (parameter-dependent) located in `path` directory.
    """
    if just_names:  # Return a list of all subdirectory names
        return [name for name in os.listdir(path)
                if os.path.isdir(os.path.join(path, name))]
    else:  # Return a list of all subdirectory paths
        return [os.path.join(path, name) for name in os.listdir(path)
                if os.path.isdir(os.path.join(path, name))]


def go_up_path(path: str, num_levels: int = 1) -> str:
    """Returns a path that has ascended `num_levels` # of parent folders.

    Args:
        path (str): Starting directory
        num_levels (int, optional): How many parent directories to ascend. Defaults to 1.

    Returns:
        str: Final parent directory
    """
    return str(Path(path).resolve().parents[num_levels-1])


def has_cosmetic(path: str) -> bool:
    """Returns True/False if the directory contains a cosmetic (.hhh) file

    Args:
        path (str): Root directory to be scanned.

    Returns:
        bool: If a cosmetic file exists, return `True`. Otherwise, return `False`.
    """
    for root, dirs, files in os.walk(path):
        for file in files:
            if file.endswith(".hhh"):
                return True
    return False
