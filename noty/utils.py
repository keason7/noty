"""Utils functions module."""

import datetime
import os

import yaml
from dotenv import load_dotenv


def check_arguments_validity(parser, args):
    """Check how many arguments are set to not None at once.

    Args:
        parser (argparse.ArgumentParser): Argparse parser.
        args (argparse.Namespace): Argparse arguments.

    Raises:
        ValueError: Maximum number of arguments=1.
    """
    # [(arg1, value1), (arg2, value2), ...]
    args_list = list(vars(args).items())
    # [value1, value2, ...]
    args_values = [arg[1] for arg in args_list]

    # all args are None, show help
    if all(value is None for value in args_values):
        parser.parse_args(["-h"])

    # Check if user launch more than one command at once
    n_args_not_none = sum(value is not None for value in args_values)

    if n_args_not_none > 1:
        raise ValueError(f"Maximum number of arguments=1, but found {n_args_not_none}")


def get_dot_env():
    """Read .env file.

    Raises:
        FileNotFoundError: Missing .env file.

    Returns:
        dict: File content.
    """
    dot_env = load_dotenv()

    if not dot_env:
        raise FileNotFoundError("Missing .env file.")

    return {"path_root": os.getenv("path_root"), "text_editor": os.getenv("text_editor")}


def read_yml(path, shell=False):
    """Read YAML file. If `shell=True`, the parsed content is printed to the console using
    `exit(content)` and the program exits immediately.

    Args:
        path (str): YAML file path.
        shell (bool, optional): If True, print and exit with the parsed YAML content. Defaults to False.

    Returns:
        dict: Parsed YAML content as a dictionary.
    """
    with open(path, "r", encoding="utf-8") as f:
        content = yaml.safe_load(f)

    if shell:
        exit(content)

    return content


def parse_state(arg):
    """Check argument type to know if its None or another type.

    Args:
        arg (int | str | bool | None): Input argument.

    Returns:
        bool: Return True is arg is not None, else False
    """
    return arg is not None


def get_timestamp():
    """Return current timestamp.

    Returns:
        str: Timestamp in YYYY_MM_DD-HH_MM_SS format.
    """
    now = datetime.datetime.now()
    return now.strftime("%Y_%m_%d-%H_%M_%S_%f")
