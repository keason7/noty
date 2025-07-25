"""I/O module."""

import json
from abc import abstractmethod


class SettingsHandler:
    """Settings I/O file handler."""

    def __init__(self, settings_path, ext=".json"):
        """Initialize settings handler object.

        Args:
            settings_path (str): Settings paths.
            ext (str, optional): File extention. Defaults to ".json".
        """
        self.location = settings_path / f"settings{ext}"

        if not self.location.exists():
            metas = {"max_idx": -1, "subjects": []}

            with open(str(self.location), "w", encoding="utf-8") as f:
                json.dump(metas, f, indent=4)

    def incr(self, updt_dict):
        """Update settings during note creation.

        Args:
            updt_dict (dict): Update dictionary.

        Returns:
            int: Max index.
        """
        with open(str(self.location), "r", encoding="utf-8") as f:
            metas = json.load(f)

        # update
        metas["max_idx"] += 1
        metas["subjects"].append(updt_dict["subject"])

        with open(str(self.location), "w", encoding="utf-8") as f:
            json.dump(metas, f, indent=4)

        return metas["max_idx"]

    def decr(self, updt_dict):
        """Update settings during note deletion.

        Args:
            updt_dict (dict): Update dictionary.
        """
        with open(str(self.location), "r", encoding="utf-8") as f:
            metas = json.load(f)

        # update
        metas["subjects"].remove(updt_dict["subject"])

        with open(str(self.location), "w", encoding="utf-8") as f:
            json.dump(metas, f, indent=4)


class AbstractHandler:
    """Abstract I/O file handler."""

    def __init__(self, inner_paths, ext):
        """Initialize handler object.

        Args:
            inner_paths (dict): Dictionary of data paths.
            ext (str): File extention.
        """
        self.inner_paths = inner_paths
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

    def __init__(self, inner_paths, ext=".json"):
        """Initialize JSON handler object.

        Args:
            inner_paths (dict): Dictionary of data paths.
            ext (str, optional): File extention.. Defaults to ".json".
        """
        super().__init__(inner_paths, ext)

    def create(self, file_name, optional_metas):
        """Create a JSON file.

        Args:
            file_name (str): Filename to create.
            optional_metas (dict): Optional metadatas.
        """
        # full file path
        file_path = self.inner_paths["metas"] / str(file_name + self.ext)

        # open settings
        with open(str(self.inner_paths["settings"]), "r", encoding="utf-8") as f:
            meta = json.load(f)

        # construct metadatas
        metas = {
            "id": meta["max_idx"] + 1,
            "date": file_name,
            "subject": optional_metas["subject"],
            "path_note": str(self.inner_paths["notes"] / str(file_name + ".txt")),
        }

        # write
        with file_path.open("w", encoding="utf-8") as f:
            json.dump(metas, f, indent=4)


class TXTHandler(AbstractHandler):
    """TXT I/O file handler."""

    def __init__(self, inner_paths, ext=".txt"):
        """Initialize TXT handler object.

        Args:
            inner_paths (dict): Dictionary of data paths.
            ext (str, optional): File extention.. Defaults to ".txt".
        """
        super().__init__(inner_paths, ext)

    def create(self, file_name, optional_metas):
        """Create a TXT file.

        Args:
            file_name (str): Filename to create.
            optional_metas (dict): Optional metadatas.
        """
        # full file path
        file_path = self.inner_paths["notes"] / str(file_name + self.ext)

        # write
        with file_path.open("w", encoding="utf-8") as f:
            f.write("")
        f.close()
