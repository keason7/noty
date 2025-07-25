"""Noty entry script."""

import argparse
import sys

from noty.noty import Noty
from noty.utils import check_args, get_env_var, parse_state


def run(parser, args):
    """Run noty command.

    Args:
        parser (argparse.ArgumentParser): Argparse parser.
        args (argparse.Namespace): Argparse arguments.
    """
    env = get_env_var()
    app = Noty(env["root_path"], env["text_editor"])

    check_args(parser, args)

    # create and launch
    if parse_state(args.create):
        app.create(args.create)
        sys.exit()

    # delete
    if parse_state(args.delete):
        app.delete(args.delete)
        sys.exit()

    # launch
    if parse_state(args.launch):
        app.launch(args.launch)
        sys.exit()

    # list
    if parse_state(args.list):
        app.list()
        sys.exit()

    # search
    if parse_state(args.search):
        app.search(args.search)
        sys.exit()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run noty app.")

    parser.add_argument("--create", type=str, default=None, help="Create a note.")
    parser.add_argument("--delete", type=int, default=None, help="Delete a note.")
    parser.add_argument("--launch", type=int, default=None, help="Launch a note.")
    parser.add_argument("--list", default=None, action="store_true", help="List notes.")
    parser.add_argument("--search", type=str, default=None, help="Search a note content.")

    args = parser.parse_args()
    run(parser, args)
