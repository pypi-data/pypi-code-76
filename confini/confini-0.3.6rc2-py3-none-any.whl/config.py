import logging
import sys
import os
import tempfile
import configparser
import re
import gnupg

from .error import DecryptError

logg = logging.getLogger('confini')

current_config = None

gpg = gnupg.GPG(
    verbose=False,
    use_agent=True,
        )
gpg.encoding = 'utf-8'


def set_current(conf, description=''):
    global current_config
    logg.debug('setting current config ({})'.format(description))
    current_config = conf 


class Config:

    parser = configparser.ConfigParser(strict=True)

    def __init__(self, config_dir, env_prefix=None, decrypt=True):
        if not os.path.isdir(config_dir):
            raise OSError('{} is not a directory'.format(config_dir))
        self.dir = os.path.realpath(config_dir)
        self.required = {}
        self.censored = {}
        self.store = {}
        self.decrypt = decrypt
        self.env_prefix = None
        if env_prefix != None:
            logg.info('using prefix {} for environment variable override matches'.format(env_prefix))
            self.env_prefix = '{}_'.format(env_prefix)


    def add(self, value, constant_name, exists_ok=False):
        if self.store.get(constant_name) != None:
            if not exists_ok:
                raise AttributeError('config key {} already exists'.format(constant_name))
            else:
                logg.debug('overwriting key {}'.format(constant_name))
        self.store[constant_name] = value


    def censor(self, identifier, section=None):
        constant_name = ''
        if section != None:
            constant_name = Config.to_constant_name(identifier, section)
        else:
            constant_name = identifier
        self.censored[constant_name] = True


    def require(self, directive, section):
        if self.required.get(section) == None:
            self.required[section] = []
        self.required[section].append(directive)


    def validate(self):
        for k in self.required.keys():
            for v in self.required[k]:
                try:
                    _ = self.parser[k][v]
                except:
                    return False
        return True


    @staticmethod
    def to_constant_name(directive, section):
        return '{}_{}'.format(section.upper(), directive.upper())


    def _sections_override(self, dct, dct_description):
        for s in self.parser.sections():
            for k in self.parser[s]:
                cn = Config.to_constant_name(k, s)
                self.override(cn, self.parser[s][k], dct, dct_description)


    def dict_override(self, dct, dct_description):
        for k in dct.keys():
            try:
                self.override(k, self.store[k], dct, dct_description)
            except KeyError:
                logg.warning('override key {} have no match in config store'.format(k))


    def override(self, cn, v, dct, dct_description):
        cn_env = cn
        if self.env_prefix != None:
            cn_env = self.env_prefix + cn
        val = dct.get(cn_env)
        if val == None or val == '':
            val = self.store.get(cn, v)
        else:
            logg.info('{} {} overrides {}'.format(dct_description, cn_env, cn))
        self.add(val, cn, exists_ok=True)


    def process(self, set_as_current=False):
        """Concatenates all .ini files in the config directory attribute and parses them to memory
        """
        tmp = tempfile.NamedTemporaryFile(delete=False)
        tmpname = tmp.name
        for filename in os.listdir(self.dir):
            if re.match(r'.+\.ini$', filename) == None:
                logg.debug('skipping file {}'.format(filename))
                continue
            logg.info('reading file {}'.format(filename))
            f = open(os.path.join(self.dir, filename), 'rb')
            while 1:
                data = f.read()
                if not data:
                    break
                tmp.write(data)
            f.close()
        tmp.close()
        self.parser.read(tmpname)
        os.unlink(tmpname)
        self._sections_override(os.environ, 'environment variable')
        if set_as_current:
            set_current(self, description=self.dir)



    def _decrypt(self, k, v):
        if type(v).__name__ != 'str':
            logg.debug('entry {} is not type str'.format(k))
            return v
        if self.decrypt:
            m = re.match(r'^\!gpg\((.*)\)', v)
            if m != None:
                filename = m.group(1)
                if filename[0] != '/':
                    filename = os.path.join(self.dir, filename)
                f = open(filename, 'rb')
                logg.debug('decrypting entry {} in file {}'.format(k, f))
                d = gpg.decrypt_file(f)
                if not d.ok:
                    raise DecryptError()
                v = str(d)
                f.close()
        return v


    def get(self, k, default=None):
        v = self.store[k]
        if v == None:
            if default != None:
                logg.debug('returning default value for empty value {}'.format(k))
            return default
        if type(v).__name__ == 'str' and v == '':
            if default != None:
                logg.debug('returning default value for empty string value {}'.format(k))
                return default
            else:
                return None

        return self._decrypt(k, v)


    def all(self):
        return self.store


    def true(self, k):
        v = self.store.get(k)
        if type(v).__name__ == 'bool':
            logg.debug('entry {} is already bool'.format(k))
            return v
        d = self._decrypt(k, v)
        if d.lower() not in ['true', 'false', '0', '1', 'on', 'off']:
            raise ValueError('{} not a boolean value'.format(k))
        return d.lower() in ['true', '1', 'on']


    def __str__(self):
        ls = []
        for k in self.store.keys():
            v = ''
            try:
                _ = self.censored[k]
                v = '***'
            except:
                v = self.store[k]

            ls.append('{}={}'.format(k, v))

        return '\n'.join(ls)


    def __repr__(self):
        return "<Config '{}'>".format(self.dir)




def config_from_environment():
    config_dir = config_dir_from_environment()
    c = Config(config_dir)
    c.process()
    return c


def config_dir_from_environment():
    return os.environ.get('CONFINI_DIR')
