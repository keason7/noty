import sys
import argparse

from noty.noty import Noty
from noty.utils import get_env_var, parse_state, check_args


def main(args):
    # get env params
    env = get_env_var()

    app = Noty(
        env['root_path'],
        env['text_editor']
    )

    # check n_args
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
        app.delete(args.launch)
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

    parser = argparse.ArgumentParser()

    parser.add_argument(
        '--create',
        type=str,
        default=None,
        help='create a note'
    )

    parser.add_argument(
        '--delete',
        type=int,
        default=None,
        help='delete a note'
    )

    parser.add_argument(
        '--launch',
        type=int,
        default=None,
        help='launch a note'
    )

    parser.add_argument(
        '--list',
        default=None,
        action='store_true',
        help='list notes'
    )

    parser.add_argument(
        '--search',
        type=str,
        default=None,
        help='search a note content'
    )

    args = parser.parse_args()

    main(args)
