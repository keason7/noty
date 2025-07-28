"""Noty entry script."""

import argparse

from noty.noty import Noty
from noty.utils import check_arguments_validity, get_dot_env


def run(arguments):
    """Run noty command.

    Args:
        parser (argparse.ArgumentParser): Argparse parser.
        arguments (argparse.Namespace): Argparse arguments.
    """
    dot_env = get_dot_env()

    app = Noty(dot_env["path_root"], dot_env["text_editor"])
    app.run(arguments)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run noty app.")

    parser.add_argument("--create", type=str, default=None, help="Create a note.")
    parser.add_argument("--delete", type=int, default=None, help="Delete a note.")
    parser.add_argument("--list", default=None, action="store_true", help="List notes.")
    parser.add_argument("--search", type=str, default=None, help="Search a note content.")
    parser.add_argument("--view", type=int, default=None, help="View a note.")

    args = parser.parse_args()

    check_arguments_validity(parser, args)
    run(args)
