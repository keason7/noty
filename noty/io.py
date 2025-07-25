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
        self.location = path_settings / f"settings{ext}"

        if not self.location.exists():
            metadatas = {"max_idx": -1, "subjects": []}

            with open(str(self.location), "w", encoding="utf-8") as f:
                json.dump(metadatas, f, indent=4)

    def incr(self, updt_dict):
        """Update settings during note creation.

        Args:
            updt_dict (dict): Update dictionary.

        Returns:
            int: Max index.
        """
        with open(str(self.location), "r", encoding="utf-8") as f:
            metadatas = json.load(f)

        metadatas["max_idx"] += 1
        metadatas["subjects"].append(updt_dict["subject"])

        with open(str(self.location), "w", encoding="utf-8") as f:
            json.dump(metadatas, f, indent=4)

        return metadatas["max_idx"]

    def decr(self, updt_dict):
        """Update settings during note deletion.

        Args:
            updt_dict (dict): Update dictionary.
        """
        with open(str(self.location), "r", encoding="utf-8") as f:
            metadatas = json.load(f)

        metadatas["subjects"].remove(updt_dict["subject"])

        with open(str(self.location), "w", encoding="utf-8") as f:
            json.dump(metadatas, f, indent=4)


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
    def create(self, file_name, optional_metas):
        """Create a file.

        Args:
            file_name (str): Filename to create.
            optional_metas (dict): Optional metadatas.

        Raises:
            NotImplementedError: Method is not implemented in abstract class.
        """
        raise NotImplementedError("Method is not implemented in abstract class.")


class JSONHandler(AbstractHandler):
    """JSON I/O file handler."""

    def __init__(self, paths_inner, ext=".json"):
        """Initialize JSON handler object.

        Args:
            paths_inner (dict): Dictionary of data paths.
            ext (str, optional): File extention.. Defaults to ".json".
        """
        super().__init__(paths_inner, ext)

    def create(self, file_name, optional_metas):
        """Create a JSON file.

        Args:
            file_name (str): Filename to create.
            optional_metas (dict): Optional metadatas.
        """
        path_file = self.paths_inner["metadatas"] / str(file_name + self.ext)

        with open(str(self.paths_inner["settings"]), "r", encoding="utf-8") as f:
            meta = json.load(f)

        # construct metadatas
        metadatas = {
            "id": meta["max_idx"] + 1,
            "date": file_name,
            "subject": optional_metas["subject"],
            "path_note": str(self.paths_inner["notes"] / str(file_name + ".txt")),
        }

        with open(path_file, "w", encoding="utf-8") as f:
            json.dump(metadatas, f, indent=4)


class TXTHandler(AbstractHandler):
    """TXT I/O file handler."""

    def __init__(self, paths_inner, ext=".txt"):
        """Initialize TXT handler object.

        Args:
            paths_inner (dict): Dictionary of data paths.
            ext (str, optional): File extention.. Defaults to ".txt".
        """
        super().__init__(paths_inner, ext)

    def create(self, file_name, optional_metas):
        """Create a TXT file.

        Args:
            file_name (str): Filename to create.
            optional_metas (dict): Optional metadatas.
        """
        path_file = self.paths_inner["notes"] / str(file_name + self.ext)

        with open(path_file, "w", encoding="utf-8") as f:
            f.write("")
        f.close()
