from noty.note_manager import NoteManager


class Noty():
    '''
    Note Manager wrapper
    '''

    def __init__(self, root_path, text_editor):
        '''
        Init NoteManager object
        '''
        self.noty = NoteManager(root_path, text_editor)

    def create(self, subject):
        '''
        Create and launch
        '''
        idx = self.noty.create_note(subject)
        self.noty.launch_note(idx)

    def delete(self, idx):
        '''
        Delete a note
        '''
        self.noty.delete_note(idx)

    def launch(self, idx):
        '''
        Launch note
        '''
        self.noty.launch_note(idx)

    def list(self):
        '''
        List registered notes
        '''
        self.noty.list_notes()

    def search(self, content):
        '''
        Search content within all notes
        '''
        self.noty.search_content(content)
