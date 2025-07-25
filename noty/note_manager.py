"""Note manager module."""

import json
import os
import subprocess
from pathlib import Path

from noty.io import JSONHandler, SettingsHandler, TXTHandler
from noty.utils import get_timestamp


class NoteManager:
    """Note Manager class."""

    def __init__(self, root_path, text_editor):
        """Initialize Note Manager object.

        Args:
            root_path (str): Installation path.
            text_editor (str): Prefered text editor.
        """
        self.root_path = Path(root_path)
        self.text_editor = text_editor

        self.inner_paths = {
            "metas": self.root_path / "metas",
            "notes": self.root_path / "notes",
            "utils": self.root_path / "utils",
            "backup": self.root_path / "backup",
        }

        # check and instanciate if needed necessary dirs
        self.verify_dir_tree()
        self.settings_io = SettingsHandler(self.inner_paths["utils"])

        self.inner_paths["settings"] = self.settings_io.location

        # handlers
        self.json_io = JSONHandler(self.inner_paths)
        self.text_io = TXTHandler(self.inner_paths)

        self.exec_backup(keys=["metas", "notes", "utils"])

    def exec_backup(self, keys):
        """Perform notes backup.

        Args:
            keys (list): List of keys to perform backup on.
        """
        for key in keys:
            # run cmd
            subprocess.run(["rsync", "-ac", self.inner_paths[key], self.inner_paths["backup"]], check=True)

    def verify_dir_tree(self):
        """Verify that installation directories are created."""
        for _, value in self.inner_paths.items():
            if not value.exists():
                Path(value).mkdir(parents=True, exist_ok=True)

    def verify_subject(self, subject):
        """Check that input subject is not in existing notes.

        Args:
            subject (str): Note subject.

        Raises:
            KeyError: Subject is not available.
        """
        with open(str(self.settings_io.location), "r", encoding="utf-8") as f:
            metas = json.load(f)

        if subject in metas["subjects"]:
            raise KeyError("Subject is not available.")

    def create_note(self, subject):
        """Create a note.

        Args:
            subject (str): Note subject.

        Returns:
            int: Note idx.
        """
        # check dirs
        self.verify_dir_tree()
        self.verify_subject(subject)

        # now
        file_name = get_timestamp()

        # create note
        self.text_io.create(file_name, None)
        self.json_io.create(file_name, {"subject": subject})
        idx = self.settings_io.incr({"subject": subject})
        return idx

    def list_notes(self):
        """List existing notes."""
        files = list(self.inner_paths["metas"].glob("**/*.json"))

        for item in files:
            metas = json.load(open(str(item), "r", encoding="utf-8"))
            print(f"note id: {metas['id']}, subject: {metas['subject']}")

    def search_content(self, content, n_extra_line=1, max_res_per_file=1):
        """Search content within notes.

        Args:
            content (str): Content to search.
            n_extra_line (int, optional): Number of lines before pattern. Defaults to 1.
            max_res_per_file (int, optional): Max occurence per file. Defaults to 1.
        """
        # meta files
        files = list(self.inner_paths["metas"].glob("**/*.json"))

        for item in files:
            # open metas
            metas = json.load(open(str(item), "r", encoding="utf-8"))

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
                metas["path_note"],
            ]

            # run cmd
            std = subprocess.run(grep, check=False, capture_output=True, text=True)

            # str result
            search_result = std.stdout

            # is there pattern
            if search_result != "":
                print(f"note id: {metas['id']}, subject: {metas['subject']}")
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
        # jsons
        files = list(self.inner_paths["metas"].glob("**/*.json"))

        for _, item in enumerate(files):
            metas = json.load(open(str(item), "r", encoding="utf-8"))

            # found note
            if metas["id"] == idx:
                return {"note": metas["path_note"], "meta": str(item)}

        raise FileNotFoundError("Note does not exist.")

    def delete_note(self, idx):
        """Delete existing note.

        Args:
            idx (int): Note index.
        """
        self.verify_dir_tree()

        # get note paths
        note_paths = self.get_note(idx)

        # load its metas
        with open(str(note_paths["meta"]), "r") as f:
            note_metas = json.load(f)

        # remove subject from settings
        self.settings_io.decr({"subject": note_metas["subject"]})

        # remove note
        os.remove(note_paths["meta"])
        os.remove(note_paths["note"])

    def launch_note(self, idx):
        """Launch existing note in prefered text editor.

        Args:
            idx (int): Note index.
        """
        note_paths = self.get_note(idx)
        subprocess.run([self.text_editor, f"{note_paths['note']}"], check=False)
