import json

from abc import abstractmethod


class AbstractHandler:
    '''
    Abstract input / output file handler
    '''

    def __init__(self, inner_paths, ext):
        '''
        Initialize
        '''
        self.inner_paths = inner_paths
        self.ext = ext

    @abstractmethod
    def create(self, file_name, optional_metas):
        '''
        Create method that needs to be implmented in subclass
        '''
        raise NotImplementedError('method is not implemented in base class')


class SettingsHandler():
    '''
    JSON input / output file handler
    '''

    def __init__(self, settings_path, ext='.json'):
        '''
        Initialize
        '''

        self.location = settings_path / f'settings{ext}'

        if not self.location.exists():
            metas = {
                'max_idx': -1,
                'subjects': []
            }

            # write
            with open(str(self.location), "w") as f:
                json.dump(metas, f, indent=4)

    def incr(self, updt_dict):
        '''
        '''
        with open(str(self.location), "r") as f:
            metas = json.load(f)

        # update
        metas['max_idx'] += 1
        metas['subjects'].append(updt_dict['subject'])

        with open(str(self.location), "w") as f:
            json.dump(metas, f, indent=4)

    def decr(self, updt_dict):
        '''
        '''
        with open(str(self.location), "r") as f:
            metas = json.load(f)

        # update
        metas['subjects'].remove(updt_dict['subject'])

        with open(str(self.location), "w") as f:
            json.dump(metas, f, indent=4)


class JSONHandler(AbstractHandler):
    '''
    JSON input / output file handler
    '''

    def __init__(self, inner_paths, ext='.json'):
        '''
        Initialize
        '''
        super().__init__(inner_paths, ext)

    def create(self, file_name, optional_metas):
        '''
        Create json metadata file in metas path
        '''

        # full file path
        file_path = self.inner_paths['metas'] / str(file_name + self.ext)

        # open settings
        with open(str(self.inner_paths['settings']), "r") as f:
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
