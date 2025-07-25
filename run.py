"""Noty entry script."""

import argparse
import sys

from noty.noty import Noty
from noty.utils import check_arguments_validity, get_dot_env, parse_state


def run(arguments):
    """Run noty command.

    Args:
        parser (argparse.ArgumentParser): Argparse parser.
        arguments (argparse.Namespace): Argparse arguments.
    """
    dot_env = get_dot_env()
    app = Noty(dot_env["path_root"], dot_env["text_editor"])

    # create and launch
    if parse_state(arguments.create):
        app.create(arguments.create)
        sys.exit()

    # delete
    if parse_state(arguments.delete):
        app.delete(arguments.delete)
        sys.exit()

    # launch
    if parse_state(arguments.launch):
        app.launch(arguments.launch)
        sys.exit()

    # list
    if parse_state(arguments.list):
        app.list()
        sys.exit()

    # search
    if parse_state(arguments.search):
        app.search(arguments.search)
        sys.exit()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run noty app.")

    parser.add_argument("--create", type=str, default=None, help="Create a note.")
    parser.add_argument("--delete", type=int, default=None, help="Delete a note.")
    parser.add_argument("--launch", type=int, default=None, help="Launch a note.")
    parser.add_argument("--list", default=None, action="store_true", help="List notes.")
    parser.add_argument("--search", type=str, default=None, help="Search a note content.")

    args = parser.parse_args()

    check_arguments_validity(parser, args)
    run(args)
