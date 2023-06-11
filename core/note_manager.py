import json

from pathlib import Path

from .utils import get_timestamp


class NoteManager:
    def __init__(self, root_path, text_editor):
        self.root_path = Path(root_path)
        self.text_editor = text_editor

        self.inner_paths = {
            'metas': self.root_path / 'metas',
            'notes': self.root_path / 'notes'
        }

        self.verify_dir_tree()

    def verify_dir_tree(self):
        for key in self.inner_paths:
            Path(self.inner_paths[key]).mkdir(parents=True, exist_ok=True)

    def create_json(self, file_name, subject):
        file_path = self.inner_paths['metas'] / str(file_name + '.json')

        idx = len(list(self.inner_paths['metas'].glob('*')))

        metas = {
            'id': idx,
            'date': file_name,
            'subject': subject
        }

        with file_path.open('w') as f:
            json.dump(metas, f, indent=4)
        f.close()

    def create_txt(self, file_name):
        file_path = self.inner_paths['notes'] / str(file_name + '.txt')

        with file_path.open("w", encoding="utf-8") as f:
            f.write('')
        f.close()

    def create_note(self, subject):
        self.verify_dir_tree()

        file_name = get_timestamp()

        self.create_txt(file_name)
        self.create_json(file_name, subject)

    def list_notes(self):
        files = list(self.inner_paths['metas'].glob('**/*.json'))

        for item in files:
            print(item.stem)