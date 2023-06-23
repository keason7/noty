import os
import datetime

from dotenv import load_dotenv


def parse_state(arg):
    '''
    Return True is arg is not None, else False
    '''
    return arg is not None


def check_args(parser, args):
    '''
    Check how many args are passed
    '''
    # get args value(s)
    args = args._get_kwargs()
    values = [arg[1] for arg in args]

    # all args args are None, show help
    if not any(values) and 0 not in values:
        parser.parse_args(["-h"])

    # all None except 1 arg -> 1
    # all None              -> 0
    n_args = len(list(set(values))) - 1

    if n_args > 1:
        raise Exception(f'max n_arg = 1, but found {n_args}')


def get_timestamp():
    '''
    Return current timestamp
    '''
    dt = datetime.datetime.now()
    ts = dt.strftime('%Y_%m_%d-%H_%M_%S_%f')

    return ts


def get_env_var():
    '''
    Load env var values as dict
    '''
    res = load_dotenv()

    if not res:
        raise Exception('.env file not found')

    root_path = os.getenv('root_path')
    text_editor = os.getenv('text_editor')

    return {'root_path': root_path, 'text_editor': text_editor}
