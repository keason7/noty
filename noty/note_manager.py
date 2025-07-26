"""Note manager module."""

import json
import os
import subprocess
from pathlib import Path

from noty.io import MetadatasHandler, NoteHandler, SettingsHandler
from noty.utils import get_timestamp


class NoteManager:
    """Note Manager class."""

    def __init__(self, path_root, text_editor):
        """Initialize Note Manager object.

        Args:
            path_root (str): Installation path.
            text_editor (str): Prefered text editor.
        """
        self.path_install = (Path(path_root) / ".noty").expanduser().resolve()
        self.path_install.mkdir(mode=0o777, parents=False, exist_ok=True)
        self.text_editor = text_editor

        self.paths_inner = {
            "metadatas": self.path_install / "metadatas",
            "notes": self.path_install / "notes",
            "settings": self.path_install / "settings",
        }

        for _, value in self.paths_inner.items():
            if not value.exists():
                Path(value).mkdir(mode=0o777, parents=False, exist_ok=True)

        self.settings_io = SettingsHandler(self.paths_inner["settings"])
        self.paths_inner["settings"] = self.settings_io.path_settings

        self.json_io = MetadatasHandler(self.paths_inner)
        self.text_io = NoteHandler(self.paths_inner)

    def verify_subject(self, subject):
        """Check that input subject is not in existing notes.

        Args:
            subject (str): Note subject.

        Raises:
            KeyError: Subject is not available.
        """
        with open(str(self.paths_inner["settings"]), "r", encoding="utf-8") as f:
            settings = json.load(f)

        if subject in settings["subjects"]:
            raise KeyError("Subject is not available.")

    def create_note(self, subject):
        """Create a note.

        Args:
            subject (str): Note subject.

        Returns:
            int: Note idx.
        """
        # check subject validity
        self.verify_subject(subject)

        timestamp = get_timestamp()
        filename = f"{timestamp}_{subject}"
        self.text_io.create(filename)
        self.json_io.create(filename, {"subject": subject})

        idx = self.settings_io.incr({"subject": subject})
        return idx

    def list_notes(self):
        """List existing notes."""
        files = list(self.paths_inner["metadatas"].glob("**/*.json"))

        for item in files:
            with open(str(item), "r", encoding="utf-8") as f:
                metadatas = json.load(f)
            print(f"note id: {metadatas['id']}, subject: {metadatas['subject']}")

    def search_content(self, content, n_extra_line=1, max_res_per_file=1):
        """Search content within notes.

        Args:
            content (str): Content to search.
            n_extra_line (int, optional): Number of lines before pattern. Defaults to 1.
            max_res_per_file (int, optional): Max occurence per file. Defaults to 1.
        """
        files = list(self.paths_inner["metadatas"].glob("**/*.json"))

        for item in files:
            with open(str(item), "r", encoding="utf-8") as f:
                metadatas = json.load(f)

            # -A : display n lines before pattern
            # -B : display n lines after pattern
            # -m : max occurence per file
            # -n : show file line number
            # --color : display patter as colored
            grep = [
                "grep",
                f"-A {n_extra_line}",
                f"-B {n_extra_line}",
                f"-m {max_res_per_file}",
                "-n",
                "--color=always",
                content,
                metadatas["path_note"],
            ]
            std = subprocess.run(grep, check=False, capture_output=True, text=True)
            search_result = std.stdout

            # is there pattern
            if search_result != "":
                print(f"note id: {metadatas['id']}, subject: {metadatas['subject']}")
                print(f"{search_result}\n")

    def get_note(self, idx):
        """Get note and metadata paths from an existing note index.

        Args:
            idx (int): Note index.

        Raises:
            FileNotFoundError: Note does not exist.

        Returns:
            dict: Note and metadata dictionary.
        """
        files = list(self.paths_inner["metadatas"].glob("**/*.json"))

        for item in files:
            with open(str(item), "r", encoding="utf-8") as f:
                metadatas = json.load(f)

            # note has been found
            if metadatas["id"] == idx:
                return {"note": metadatas["path_note"], "meta": str(item)}

        raise FileNotFoundError("Note does not exist.")

    def delete_note(self, idx):
        """Delete existing note.

        Args:
            idx (int): Note index.
        """
        paths_note = self.get_note(idx)

        with open(str(paths_note["meta"]), "r", encoding="utf-8") as f:
            metadatas = json.load(f)

        # remove subject from settings
        self.settings_io.decr({"subject": metadatas["subject"]})

        # remove note
        os.remove(paths_note["meta"])
        os.remove(paths_note["note"])

    def launch_note(self, idx):
        """Launch existing note in prefered text editor.

        Args:
            idx (int): Note index.
        """
        paths_note = self.get_note(idx)
        subprocess.run([self.text_editor, f"{paths_note['note']}"], check=False)
