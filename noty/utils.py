"""Utils functions module."""

import datetime
import os

import yaml
from dotenv import load_dotenv


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


def check_args(parser, args):
    """Check how many arguments are passed.

    Args:
        parser (argparse.ArgumentParser): Argparse parser.
        args (argparse.Namespace): Argparse arguments.

    Raises:
        ValueError: Maximum number of arguments=1.
    """
    # get args value(s)
    values = [arg[1] for arg in args._get_kwargs()]

    # all args args are None, show help
    if not any(values) and 0 not in values:
        parser.parse_args(["-h"])

    # all None except 1 arg -> 1
    # all None              -> 0
    n_args = len(list(set(values))) - 1

    if n_args > 1:
        raise ValueError(f"Maximum number of arguments=1, but found {n_args}")


def get_timestamp():
    """Return current timestamp.

    Returns:
        str: Timestamp in YYYY_MM_DD-HH_MM_SS format.
    """
    now = datetime.datetime.now()
    return now.strftime("%Y_%m_%d-%H_%M_%S_%f")


def get_env_var():
    """Read .env file.

    Raises:
        FileNotFoundError: Missing .env file.

    Returns:
        dict: File content.
    """
    dotenv = load_dotenv()

    if not dotenv:
        raise FileNotFoundError("Missing .env file.")

    return {"root_path": os.getenv("root_path"), "text_editor": os.getenv("text_editor")}
