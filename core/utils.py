import os
import datetime

from dotenv import load_dotenv


def get_timestamp():
    dt = datetime.datetime.now()
    ts = dt.strftime('%Y_%m_%d-%H_%M_%S')

    return ts


def get_env_var():
    res = load_dotenv()

    if not res:
        raise Exception('.env file not found')

    root_path = os.getenv('root_path')
    text_editor = os.getenv('text_editor')

    return {'root_path': root_path, 'text_editor': text_editor}
