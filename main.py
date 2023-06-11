from core.utils import get_env_var
from core.note_manager import NoteManager


def main():
    env = get_env_var()

    noty = NoteManager(env['root_path'], env['text_editor'])

    noty.create_note('a')

    noty.list_notes()


if __name__ == "__main__":
    main()
