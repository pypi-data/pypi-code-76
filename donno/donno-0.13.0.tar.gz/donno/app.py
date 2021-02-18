import fire
from donno import notes, config
from donno import converters
from pprint import pprint


class App:
    def add(self):
        '''Add a new note in the current notebook. Abbr: a'''
        notes.add_note()

    def a(self):
        """Alias of add command"""
        self.add()

    def advanced_search(self, name: str = '', tag: str = '',
                        content: str = '', book: str = ''):
        '''advanced search with title(naem), tag, notebook and content
        Abbr: ads
        :param name: string in note title (name)
        :param tag: string in note tag
        :param content: string in note body
        :param book: string in notebook
        '''
        print(notes.advanced_search(name, tag, content, book))

    def ads(self, name: str = '', tag: str = '',
            content: str = '', book: str = ''):
        '''alias for advanced-search command
        '''
        self.advanced_search(name, tag, content, book)

    def backup(self, comments: str = "update notes"):
        '''Backup notes to remote repository. Abbr: b
        '''
        notes.backup_repo(comments)

    def b(self, comments: str = "update notes"):
        '''alias for backup command
        '''
        self.backup(comments)

    def conf(self, action, *params):
        """Manage configurations
        :param action: get|set|restore
        :param params: [attribute name, attribute value]
        """
        if action == "get":
            pprint(config.get_attr(params), indent=2)
        elif action == "set":
            pprint(config.set_attr(params), indent=2)
        elif action == "restore":
            pprint(config.restore(), indent=2)
        else:
            print(f"Invalid action: {action}")

    def delete(self, no):
        '''Delete the <no>th note
        :param no: no. of note to delete
        '''
        notes.delete_note(no)

    def edit(self, no=1):
        '''Edit the <no>th note. Abbr: e
        :param no: no. of note to edit, default: 1
        '''
        notes.update_note(no)

    def exports(self, ftype='json'):
        '''Export all notes into an external file
        :param ftype: export file type, default: JSON
        '''
        notes.export_notes(ftype)

    def e(self, no=1):
        '''Alias of edit command'''
        self.edit(no)

    def imports(self, notes_folder, source_type):
        if source_type == 'joplin':
            converters.joplin.import_json(notes_folder)

    def list(self, number=5):
        '''List most updated <number> notes. Abbr: l
        :param number: number of note to edit, default: 5
        '''
        print(notes.list_notes(number))

    def l(self, number=5):  # noqa
        """Alias of list command"""
        self.list(number)

    def list_notebooks(self):
        '''List notebooks. Abbr: lnb
        '''
        print(notes.list_notebooks())

    def lnb(self):
        '''alias for list-notebook command
        '''
        self.list_notebooks()

    def pv(self, no=1):
        '''Render note as HTML and preview in browser'''
        notes.preview_note(no)

    def search(self, *keys):
        '''Search by keys in all notes. Abbr: s
        :param keys: list of keywords to search
        '''
        print(notes.simple_search(keys))

    def s(self, *keys):
        '''alias for search command'''
        self.search(*keys)

    def view(self, no=1):
        '''View the <no>th note. Abbr: v
        :param no: no. of note to edit, default: 1
        '''
        notes.view_note(no)

    def v(self, no=1):
        '''Alias of view command'''
        self.view(no)


def main():
    fire.Fire(App)


# for test purpose:
# python donno/app.py s python con
if __name__ == '__main__':
    main()
