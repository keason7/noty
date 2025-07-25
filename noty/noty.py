"""Noty module."""

from noty.note_manager import NoteManager


class Noty:
    """Note Manager commands wrapper."""

    def __init__(self, path_root, text_editor):
        """Initialize Noty object.

        Args:
            path_root (str): Installation path.
            text_editor (str): Prefered text editor.
        """
        self.noty = NoteManager(path_root, text_editor)

    def create(self, subject):
        """Create and launch a note.

        Args:
            subject (str): Subject of the note.
        """
        idx = self.noty.create_note(subject)
        self.noty.launch_note(idx)

    def delete(self, idx):
        """Delete a note.

        Args:
            idx (int): Note id.
        """
        self.noty.delete_note(idx)

    def launch(self, idx):
        """Launch a note.

        Args:
            idx (int): Note id.
        """
        self.noty.launch_note(idx)

    def list(self):
        """List existing notes."""
        self.noty.list_notes()

    def search(self, content):
        """Search content within all existing notes.

        Args:
            content (str): String to search.
        """
        self.noty.search_content(content)
