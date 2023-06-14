import json

from abc import abstractmethod


class AbstractHandler:
    '''
    Abstract input / output file handler
    '''

    def __init__(self, inner_paths, ext, setting_file='global'):
        '''
        Initialize
        '''
        self.inner_paths = inner_paths
        self.ext = ext
        self.setting_file = setting_file

    @abstractmethod
    def create(self, file_name, optional_metas):
        '''
        Create method that needs to be implmented in subclass
        '''
        raise NotImplementedError('method is not implemented in base class')


class JSONHandler(AbstractHandler):
    '''
    JSON input / output file handler
    '''

    def __init__(self, inner_paths, ext='.json'):
        '''
        Initialize
        '''
        super().__init__(inner_paths, ext)

        self.check_setting_file()

    def create(self, file_name, optional_metas):
        '''
        Create json metadata file in metas path
        '''

        # full file path
        file_path = self.inner_paths['metas'] / str(file_name + self.ext)
        setting_path = self.inner_paths['utils'] / str(self.setting_file + self.ext)

        # open settings
        with open(str(setting_path), "r") as f:
            meta = json.load(f)

        # construct metadatas
        metas = {
            'id': meta['max_idx'] + 1,
            'date': file_name,
            'subject': optional_metas['subject'],
            'path_note': str(self.inner_paths['notes'] / str(file_name + '.txt'))
        }

        # write
        with file_path.open('w') as f:
            json.dump(metas, f, indent=4)

        # update settings
        self.update_setting_file(optional_metas['subject'])

    def check_setting_file(self):
        '''
        Check setting file existance and eventually create it
        '''
        file_path = self.inner_paths['utils'] / str(self.setting_file + self.ext)

        if not file_path.exists():
            metas = {
                'max_idx': -1,
                'subjects': []
            }

            # write
            with open(str(file_path), "w") as f:
                json.dump(metas, f, indent=4)

    def update_setting_file(self, subject):
        '''
        Update setting file after a not creation
        '''
        file_path = self.inner_paths['utils'] / str(self.setting_file + self.ext)

        with open(str(file_path), "r") as f:
            metas = json.load(f)

        # update
        metas['max_idx'] += 1
        metas['subjects'].append(subject)

        with open(str(file_path), "w") as f:
            json.dump(metas, f, indent=4)


class TXTHandler(AbstractHandler):
    '''
    TXT input / output file handler
    '''

    def __init__(self, inner_paths, ext='.txt'):
        '''
        Initialize
        '''
        super().__init__(inner_paths, ext)

    def create(self, file_name, optional_metas):
        '''
        Create txt note file in notes path
        '''

        # full file path
        file_path = self.inner_paths['notes'] / str(file_name + self.ext)

        # write
        with file_path.open("w", encoding="utf-8") as f:
            f.write('')
        f.close()
