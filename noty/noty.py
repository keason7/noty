"""Noty module."""

import sys

from noty.note_manager import NoteManager
from noty.utils import parse_arg_state


class Noty:
    """Note Manager commands wrapper."""

    def __init__(self, path_root, text_editor):
        """Initialize Noty object.

        Args:
            path_root (str): Installation path.
            text_editor (str): Prefered text editor.
        """
        self.note_manager = NoteManager(path_root, text_editor)

    def create(self, subject):
        """Create and launch a note.

        Args:
            subject (str): Subject of the note.
        """
        idx = self.note_manager.create_note(subject)
        self.note_manager.launch_note(idx)

    def delete(self, idx):
        """Delete a note.

        Args:
            idx (int): Note id.
        """
        self.note_manager.delete_note(idx)

    def launch(self, idx):
        """Launch a note.

        Args:
            idx (int): Note id.
        """
        self.note_manager.launch_note(idx)

    def list(self):
        """List existing notes."""
        self.note_manager.list_notes()

    def search(self, content):
        """Search content within all existing notes.

        Args:
            content (str): String to search.
        """
        self.note_manager.search_content(content)

    def run(self, args):
        """Run a noty command.

        Args:
            args (argparse.Namespace): Argparse arguments.
        """
        # create and launch
        if parse_arg_state(args.create):
            self.create(args.create)
            sys.exit()

        # delete
        if parse_arg_state(args.delete):
            self.delete(args.delete)
            sys.exit()

        # launch
        if parse_arg_state(args.launch):
            self.launch(args.launch)
            sys.exit()

        # list
        if parse_arg_state(args.list):
            self.list()
            sys.exit()

        # search
        if parse_arg_state(args.search):
            self.search(args.search)
            sys.exit()
