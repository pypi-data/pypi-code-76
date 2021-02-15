import io
import logging
import os
import shutil
import uuid

import ruamel.yaml
import xapian
import jinja2

from pkg_resources import resource_string
from . import types

try:
    import git

    git_available = True
except ImportError:
    git_available = False


class Entry(object):
    def __init__(self, collection, data={}, fname=None):
        self.collection = collection
        self.data = data or self.empty_data()
        self.fname = fname
        self.eid = self.data.get('eid', None)
        if not self.eid:
            if self.fname:
                self.eid, ext = os.path.splitext(os.path.basename(self.fname))
            else:
                self.eid = uuid.uuid4().hex
        if not self.fname:
            self.fname = self.eid + '.yaml'

    def __str__(self):
        label = self.collection.settings.get('entry_label', None)
        if label:
            t = jinja2.Template(label)
            return t.render(**self.get_data())
        else:
            return self.eid

    def get_data(self):
        d = self.data.copy()
        d['eid'] = self.eid
        d['fname'] = self.fname
        d['short_id'] = self.short_id
        return d

    def empty_data(self):
        data = self.collection.yaml.load("{}")
        for name, field in self.collection.fields.items():
            if field.field.get('default', None):
                data[name] = field.field['default']
            else:
                data[name] = field.empty()
            if field.field.get('help', None) is not None:
                comment = "# {name} ({type}): {help}\n".format(**field.field)
                try:
                    data.yaml_set_comment_before_after_key(
                        key=name,
                        before=comment,
                        indent=0
                    )
                except AttributeError:
                    logging.warning(
                        "Not adding comments because they are not"
                        "supported by the yaml loader."
                    )
        return data

    @property
    def yaml_data(self):
        to_dump = self.data.copy()
        # Decimal fields can't be represented by
        # ruamel.yaml.RoundTripDumper, but transforming them to strings
        # should be enough for all cases that we need.
        for field in self.collection.settings['fields']:
            if field['type'] == 'decimal':
                v = to_dump.get(field['name'], '')
                if v is not None:
                    to_dump[field['name']] = str(v)

        s_io = io.StringIO()
        self.collection.yaml.dump(to_dump, s_io)
        return s_io.getvalue()

    @property
    def idterm(self):
        return "Q" + self.eid

    @property
    def short_id(self):
        return self.eid[:8]

    def validate(self):
        errors = []
        valid = True
        for name, field in self.collection.fields.items():
            value = self.data.get(name, None)
            try:
                self.data[name] = field.load(value)
            except types.LesanaValueError as e:
                valid = False
                errors.append(
                    {
                        'field': name,
                        'error': e,
                    }
                )
        return valid, errors

    def render(self, template, searchpath='.'):
        jtemplate = self.collection.get_template(template, searchpath)
        try:
            return jtemplate.render(entry=self)
        except jinja2.exceptions.TemplateSyntaxError as e:
            raise TemplatingError('Template Syntax Error: ' + str(e))

    def auto(self):
        """
        Update all fields of this entry, as required by the field settings.

        This is called by the reference client before an edit, so that
        the user can make further changes.

        Note that the stored file is not changed: if you need it you
        need to save the entry yourself.
        """
        for name, field in self.collection.fields.items():
            self.data[name] = field.auto(self.data.get(name, None))


class Collection(object):
    """
    """

    PARSER_FLAGS = (
        xapian.QueryParser.FLAG_BOOLEAN
        | xapian.QueryParser.FLAG_PHRASE  # noqa: W503
        | xapian.QueryParser.FLAG_LOVEHATE  # noqa: W503
        | xapian.QueryParser.FLAG_WILDCARD  # noqa: W503
    )

    def __init__(self, directory=None, itemdir='items'):
        self.basedir = directory or os.getcwd()
        self.itemdir = os.path.join(self.basedir, itemdir)
        self.yaml = ruamel.yaml.YAML()
        self.yaml.preserve_quotes = True
        self.yaml.typ = 'rt'
        try:
            with open(os.path.join(self.basedir, 'settings.yaml')) as fp:
                self.settings = self.yaml.load(fp)
        except FileNotFoundError:
            self.settings = self.yaml.load("{}")
        self.fields = self._load_field_types()
        os.makedirs(os.path.join(self.basedir, '.lesana'), exist_ok=True)
        if 'lang' in self.settings:
            try:
                self.stemmer = xapian.Stem(self.settings['lang'])
            except xapian.InvalidArgumentError:
                logging.warning(
                    "Invalid language %s, in settings.yaml: using english.",
                    self.settings['lang'],
                )
                self.stemmer = xapian.Stem('english')
        else:
            self.stemmer = xapian.Stem('english')
        self._enquire = None
        self.entry_class = Entry

    def _get_subsubclasses(self, cls):
        for c in cls.__subclasses__():
            yield c
            yield from self._get_subsubclasses(c)

    def _load_field_types(self):
        type_loaders = {}
        for t in self._get_subsubclasses(types.LesanaType):
            type_loaders[t.name] = t
        fields = {}
        for i, field in enumerate(self.settings.get('fields', [])):
            try:
                fields[field['name']] = type_loaders[field['type']](
                    field,
                    type_loaders,
                    # value slot 0 is used to store the filename, and we
                    # reserve a few more slots just in case they are
                    # needed by lesana or some derivative
                    value_index=i + 16,
                )
            except KeyError:
                # unknown fields are treated as if they were
                # (unvalidated) generic YAML to support working with
                # collections based on lesana derivatives
                logging.warning(
                    "Unknown field type %s in field %s",
                    field['type'],
                    field['name'],
                )
                fields[field['name']] = types.LesanaYAML(field, type_loaders)
        return fields

    def _index_file(self, fname, cache):
        with open(os.path.join(self.itemdir, fname)) as fp:
            data = self.yaml.load(fp)
        entry = self.entry_class(self, data, fname)
        valid, errors = entry.validate()
        if not valid:
            logging.warning(
                "Not indexing {fname}: invalid data".format(fname=fname)
            )
            return False, errors

        doc = xapian.Document()
        self.indexer.set_document(doc)

        for field, loader in self.fields.items():
            loader.index(doc, self.indexer, entry.data.get(field))

        doc.set_data(entry.yaml_data)
        doc.add_boolean_term(entry.idterm)
        doc.add_value(0, entry.fname.encode('utf-8'))

        cache.replace_document(entry.idterm, doc)
        return True, []

    @property
    def indexed_fields(self):
        fields = []
        for field in self.settings['fields']:
            if field.get('index', '') in ['free', 'field']:
                prefix = field.get('prefix', 'X' + field['name'].upper())
                fields.append(
                    {
                        'prefix': prefix,
                        'name': field['name'],
                        'free_search': field['index'] == 'free',
                        'multi': field['type'] in ['list'],
                    }
                )
        return fields

    def update_cache(self, fnames=None, reset=False):
        """
        Update the xapian db with the data in files.

        ``fnames`` is a list of *basenames* of files in ``self.itemdir``.

        If no files have been passed, add everything.

        if ``reset`` the existing xapian db is deleted before indexing

        Return the number of files that have been added to the cache.
        """
        if reset:
            shutil.rmtree(os.path.join(self.basedir, '.lesana'))
        os.makedirs(os.path.join(self.basedir, '.lesana'), exist_ok=True)
        cache = xapian.WritableDatabase(
            os.path.join(self.basedir, '.lesana/xapian'),
            xapian.DB_CREATE_OR_OPEN,
        )
        self.indexer = xapian.TermGenerator()
        self.indexer.set_stemmer(self.stemmer)
        if not fnames:
            try:
                fnames = os.listdir(self.itemdir)
            except FileNotFoundError:
                logging.warning(
                    "No such file or directory: {}, not updating cache".format(
                        self.itemdir
                    )
                )
                return 0
        updated = 0
        for fname in fnames:
            try:
                valid, errors = self._index_file(fname, cache)
            except IOError as e:
                logging.warning(
                    "Could not load file {}: {}".format(fname, str(e))
                )
            else:
                if valid:
                    updated += 1
                else:
                    logging.warning(
                        "File {fname} could not be indexed: {errors}".format(
                            fname=fname, errors=errors
                        )
                    )
        return updated

    def save_entries(self, entries=[]):
        for e in entries:
            complete_name = os.path.join(self.itemdir, e.fname)
            with open(complete_name, 'w') as fp:
                fp.write(e.yaml_data)

    def git_add_files(self, files=[]):
        if not git_available:
            logging.warning(
                "python3-git not available, could not initalise "
                + "the git repository."  # noqa: W503
            )
            return False
        if not self.settings.get('git', False):
            logging.info("This collection is configured not to use git")
            return False
        try:
            repo = git.Repo(self.basedir, search_parent_directories=True)
        except git.exc.InvalidGitRepositoryError:
            logging.warning(
                "Could not find a git repository in {}".format(self.basedir)
            )
            return False
        repo.index.add(files)
        return True

    def _get_cache(self):
        try:
            cache = xapian.Database(
                os.path.join(self.basedir, '.lesana/xapian'),
            )
        except xapian.DatabaseOpeningError:
            logging.info("No database found, indexing entries.")
            self.update_cache()
            cache = xapian.Database(
                os.path.join(self.basedir, '.lesana/xapian'),
            )
        return cache

    def start_search(self, querystring, sort_by=None):
        """
        Prepare a search for querystring.
        """
        cache = self._get_cache()
        queryparser = xapian.QueryParser()
        queryparser.set_stemmer(self.stemmer)
        queryparser.set_database(cache)

        for field in self.indexed_fields:
            queryparser.add_prefix(field['name'], field['prefix'])

        if querystring == '*':
            query = xapian.Query.MatchAll
        else:
            query = queryparser.parse_query(querystring, self.PARSER_FLAGS)

        self._enquire = xapian.Enquire(cache)
        self._enquire.set_query(query)

        if not sort_by and self.settings.get('default_sort', False):
            sort_by = self.settings['default_sort']

        if sort_by:
            keymaker = xapian.MultiValueKeyMaker()
            for k in sort_by:
                if k.startswith('+'):
                    reverse = False
                    slot = self.fields[k[1:]].value_index
                elif k.startswith('-'):
                    reverse = True
                    slot = self.fields[k[1:]].value_index
                else:
                    reverse = False
                    slot = self.fields[k].value_index
                keymaker.add_value(slot, reverse)
            self._enquire.set_sort_by_key_then_relevance(keymaker, False)

    def get_search_results(self, offset=0, pagesize=12):
        if not self._enquire:
            return
        for match in self._enquire.get_mset(offset, pagesize):
            yield self._match_to_entry(match)

    def get_all_search_results(self):
        if not self._enquire:
            return
        offset = 0
        pagesize = 100
        while True:
            mset = self._enquire.get_mset(offset, pagesize)
            if mset.size() == 0:
                break
            for match in mset:
                yield self._match_to_entry(match)
            offset += pagesize

    def get_all_documents(self):
        """
        Yield all documents in the collection.

        Note that the results can't be sorted, even if the collection
        has a default_sort; if you need sorted values you need to use a
        regular search with a query of '*'
        """
        cache = self._get_cache()
        postlist = cache.postlist("")
        for post in postlist:
            doc = cache.get_document(post.docid)
            yield self._doc_to_entry(doc)

    def _match_to_entry(self, match):
        return self._doc_to_entry(match.document)

    def _doc_to_entry(self, doc):
        fname = doc.get_value(0).decode('utf-8')
        data = self.yaml.load(doc.get_data())
        entry = self.entry_class(self, data=data, fname=fname,)
        return entry

    def entry_from_eid(self, eid):
        cache = self._get_cache()
        postlist = cache.postlist('Q' + eid)
        for pitem in postlist:
            return self._doc_to_entry(cache.get_document(pitem.docid))
        return None

    def entries_from_short_eid(self, seid):
        # It would be better to search for partial UIDs inside xapian,
        # but I still can't find a way to do it, so this is a workable
        # workaround on repos where the eids are stored in the
        # filenames.
        potential_eids = [
            os.path.splitext(f)[0]
            for f in os.listdir(self.itemdir)
            if f.startswith(seid)
        ]
        return [self.entry_from_eid(u) for u in potential_eids if u]

    def remove_entries(self, eids):
        cache = xapian.WritableDatabase(
            os.path.join(self.basedir, '.lesana/xapian'),
            xapian.DB_CREATE_OR_OPEN,
        )
        for eid in eids:
            for entry in self.entries_from_short_eid(eid):
                if entry is not None:
                    cache.delete_document(entry.idterm)
                    self.remove_file(entry.fname)
                else:
                    logging.warning("No such entry: {}, ignoring".format(eid))
        cache.commit()
        cache.close()

    def remove_file(self, fname):
        f_path = os.path.join(self.itemdir, fname)
        if git_available and self.settings.get('git', False):
            try:
                repo = git.Repo(self.basedir, search_parent_directories=True)
            except git.exc.InvalidGitRepositoryError:
                logging.warning(
                    "Could not find a git repository in {}".format(
                        self.basedir
                    )
                )
                return False
            repo.index.remove([f_path])
        os.remove(f_path)

    def update_field(self, query, field, value):
        self.start_search(query)
        changed = []
        for e in self.get_all_search_results():
            e.data[field] = value
            changed.append(e)
        self.save_entries(changed)
        self.git_add_files(
            [os.path.join(self.itemdir, e.fname) for e in changed]
        )
        self.update_cache([e.fname for e in changed])

    def get_template(self, template_fname, searchpath='.'):
        env = jinja2.Environment(
            loader=jinja2.FileSystemLoader(
                searchpath=searchpath, followlinks=True,
            ),
            # TODO: add autoescaping settings
        )
        try:
            template = env.get_template(template_fname)
        except jinja2.exceptions.TemplateNotFound as e:
            raise TemplatingError('Could not find template' + str(e))
        return template

    @classmethod
    def init(
        cls, directory=None, git_enabled=True, edit_file=None, settings={}
    ):
        """
        Initialize a lesana repository

        directory defaults to .
        if git_enabled is True, git support is enabled and if possible a git
        repository is initalized.
        edit_file is a syncronous function that runs on a filename
        (possibly opening the file in an editor) and should manage its
        own errors.
        """
        c_dir = os.path.abspath(directory or '.')
        os.makedirs(c_dir, exist_ok=True)
        if git_enabled:
            # Try to initalize a git repo
            if git_available:
                repo = git.Repo.init(c_dir, bare=False)
            else:
                logging.warning(
                    "python3-git not available, could not initalise "
                    + "the git repository."  # noqa: W503
                )
                repo = None
            # Add .lesana directory to .gitignore and add it to the
            # staging
            lesana_ignored = False
            try:
                with open(os.path.join(c_dir, '.gitignore'), 'r') as fp:
                    for line in fp:
                        if '.lesana' in line:
                            lesana_ignored = True
                            continue
            except FileNotFoundError:
                pass
            if not lesana_ignored:
                with open(os.path.join(c_dir, '.gitignore'), 'a') as fp:
                    fp.write('#Added by lesana init\n.lesana')
                if repo:
                    repo.index.add(['.gitignore'])
            # TODO: Add hook to index files as they are pulled
        # If it doesn't exist, create a skeleton of settings.yaml file
        # then open settings.yaml for editing
        filepath = os.path.join(c_dir, 'settings.yaml')
        if not os.path.exists(filepath):
            skel = resource_string('lesana', 'data/settings.yaml').decode(
                'utf-8'
            )
            yaml = ruamel.yaml.YAML()
            skel_dict = yaml.load(skel)
            skel_dict['git'] = git_enabled
            skel_dict.update(settings)
            with open(filepath, 'w') as fp:
                yaml.dump(skel_dict, stream=fp)
        if edit_file:
            edit_file(filepath)
        if git_enabled and repo:
            repo.index.add(['settings.yaml'])
        coll = cls(c_dir)
        os.makedirs(os.path.join(coll.basedir, coll.itemdir), exist_ok=True)
        return coll


class TemplatingError(Exception):
    """
    Raised when there are errors rendering a jinja template
    """
