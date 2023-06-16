import os
import json
import subprocess

from pathlib import Path

from .utils import get_timestamp
from .io import TXTHandler, JSONHandler, SettingsHandler


class NoteManager:
    def __init__(self, root_path, text_editor):
        '''
        Initialize
        '''
        self.root_path = Path(root_path)
        self.text_editor = text_editor

        self.inner_paths = {
            'metas': self.root_path / 'metas',
            'notes': self.root_path / 'notes',
            'utils': self.root_path / 'utils'
        }

        # check and instanciate if needed necessary dirs
        self.verify_dir_tree()
        self.settings_io = SettingsHandler(self.inner_paths['utils'])

        self.inner_paths['settings'] = self.settings_io.location

        # handlers
        self.json_io = JSONHandler(self.inner_paths)
        self.text_io = TXTHandler(self.inner_paths)

    def verify_dir_tree(self):
        '''
        Check or create main dirs
        '''
        for key in self.inner_paths:
            if not self.inner_paths[key].exists():
                Path(self.inner_paths[key]).mkdir(parents=True, exist_ok=True)

    def verify_subject(self, subject):
        '''
        Check if subject is already within an existing note
        '''

        with open(str(self.settings_io.location), "r") as f:
            metas = json.load(f)

        if subject in metas['subjects']:
            raise Exception('subject is not available')

    def create_note(self, subject):
        '''
        Create a note with meta file
        '''

        # check dirs
        self.verify_dir_tree()
        self.verify_subject(subject)

        # now
        file_name = get_timestamp()

        # create note
        self.text_io.create(file_name, None)
        self.json_io.create(file_name, {'subject': subject})
        self.settings_io.incr({'subject': subject})

    def list_notes(self):
        pass

    def get_note(self, idx):
        '''
        Get note / meta paths from an existing note
        '''

        # jsons
        files = list(self.inner_paths['metas'].glob('**/*.json'))

        for _, item in enumerate(files):
            metas = json.load(open(str(item)))

            # found note
            if metas['id'] == idx:
                return {'note': metas['path_note'], 'meta': str(item)}

        raise Exception('Note does not exist')

    def delete_note(self, idx):
        '''
        Remove existing note
        '''
        self.verify_dir_tree()

        # get note paths
        note_paths = self.get_note(idx)

        # load its metas
        with open(str(note_paths['meta']), "r") as f:
            note_metas = json.load(f)

        # remove subject from settings
        self.settings_io.decr({'subject': note_metas['subject']})

        # remove note
        os.remove(note_paths['meta'])
        os.remove(note_paths['note'])

    def launch_note(self, idx):
        '''
        Launch existing note in text editor
        '''
        note_paths = self.get_note(idx)
        subprocess.run([self.text_editor, f"{note_paths['note']}"])
