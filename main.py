import sys
import argparse

from noty.utils import get_env_var
from noty.note_manager import NoteManager


def parse_state(arg):
    return arg is not None


def check_args(args):
    args = args._get_kwargs()
    values = [arg[1] for arg in args]

    if not any(values) and 0 not in values:
        parser.parse_args(["-h"])

    n_args = len(list(set(values))) - 1

    if n_args > 1:
        raise Exception(f'max n_arg = 1, but found {n_args}')


class Launcher():
    def __init__(self):
        env = get_env_var()
        self.noty = NoteManager(env['root_path'], env['text_editor'])

    def create(self, subject):
        idx = self.noty.create_note(subject)
        self.noty.launch_note(idx)

    def delete(self, idx):
        self.noty.delete_note(idx)

    def launch(self, idx):
        self.noty.launch_note(idx)

    def list(self):
        self.noty.list_notes()


if __name__ == "__main__":

    app = Launcher()

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

    check_args(args)

    if parse_state(args.create):
        app.create(args.create)
        sys.exit()

    if parse_state(args.delete):
        app.delete(args.delete)
        sys.exit()

    if parse_state(args.launch):
        app.delete(args.launch)
        sys.exit()

    if parse_state(args.list):
        app.list()
        sys.exit()

    if parse_state(args.search):
        app.search(args.search)
        sys.exit()
