"""I/O module."""

import json
from abc import abstractmethod


class SettingsHandler:
    """Settings I/O file handler."""

    def __init__(self, path_settings, ext=".json"):
        """Initialize settings handler object.

        Args:
            path_settings (str): Settings paths.
            ext (str, optional): File extention. Defaults to ".json".
        """
        self.path_settings = path_settings / f"settings{ext}"

        if not self.path_settings.exists():
            with open(str(self.path_settings), "w", encoding="utf-8") as f:
                json.dump({"max_idx": -1, "titles": []}, f)

    def incr(self, updt_dict):
        """Update settings during note creation.

        Args:
            updt_dict (dict): Update dictionary.

        Returns:
            int: Max index.
        """
        with open(str(self.path_settings), "r", encoding="utf-8") as f:
            settings = json.load(f)

        settings["max_idx"] += 1
        settings["titles"].append(updt_dict["title"])

        with open(str(self.path_settings), "w", encoding="utf-8") as f:
            json.dump(settings, f)

        return settings["max_idx"]

    def decr(self, updt_dict):
        """Update settings during note deletion.

        Args:
            updt_dict (dict): Update dictionary.
        """
        with open(str(self.path_settings), "r", encoding="utf-8") as f:
            settings = json.load(f)

        settings["titles"].remove(updt_dict["title"])

        with open(str(self.path_settings), "w", encoding="utf-8") as f:
            json.dump(settings, f)


class AbstractHandler:
    """Abstract I/O file handler."""

    def __init__(self, paths_inner, ext):
        """Initialize handler object.

        Args:
            paths_inner (dict): Dictionary of data paths.
            ext (str): File extention.
        """
        self.paths_inner = paths_inner
        self.ext = ext

    @abstractmethod
    def create(self, file_name, optional_metas=None):
        """Create a file.

        Args:
            file_name (str): Filename to create.
            optional_metas (dict): Optional metadatas.

        Raises:
            NotImplementedError: Method is not implemented in abstract class.
        """
        raise NotImplementedError("Method is not implemented in abstract class.")


class NoteHandler(AbstractHandler):
    """Note I/O file handler."""

    def __init__(self, paths_inner, ext=".txt"):
        """Initialize note handler object.

        Args:
            paths_inner (dict): Dictionary of data paths.
            ext (str, optional): File extention.. Defaults to ".txt".
        """
        super().__init__(paths_inner, ext)

    def create(self, file_name, optional_metas=None):
        """Create a note file.

        Args:
            file_name (str): Filename to create.
            optional_metas (dict): Optional metadatas.
        """
        path_file = self.paths_inner["notes"] / str(file_name + self.ext)

        with open(path_file, "w", encoding="utf-8") as f:
            f.write("")
        f.close()


class MetadatasHandler(AbstractHandler):
    """Metadatas I/O file handler."""

    def __init__(self, paths_inner, ext=".json"):
        """Initialize metadatas handler object.

        Args:
            paths_inner (dict): Dictionary of data paths.
            ext (str, optional): File extention.. Defaults to ".json".
        """
        super().__init__(paths_inner, ext)

    def create(self, file_name, optional_metas=None):
        """Create a metadatas file.

        Args:
            file_name (str): Filename to create.
            optional_metas (dict): Optional metadatas.
        """
        path_file = self.paths_inner["metadatas"] / str(file_name + self.ext)

        with open(str(self.paths_inner["settings"]), "r", encoding="utf-8") as f:
            settings = json.load(f)

        # construct metadatas
        metadatas = {
            "id": settings["max_idx"] + 1,
            "date": file_name,
            "title": optional_metas["title"],
            "path_note": str(self.paths_inner["notes"] / str(file_name + ".txt")),
        }

        with open(path_file, "w", encoding="utf-8") as f:
            json.dump(metadatas, f)
