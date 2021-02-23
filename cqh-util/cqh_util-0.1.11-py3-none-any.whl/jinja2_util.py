import logging
from os import path
from hashlib import md5
from jinja2.bccache import FileSystemBytecodeCache, Bucket


class LocalFileSystemBytecodeCache(FileSystemBytecodeCache):
    '''
    例子

    class TemplateRendring(object):
        """
        A simple class to hold methods for rendering templates.
        """

        @classmethod
        def template_env(cls):
            if not hasattr(cls, '_template_env'):
                template_dirs = []
                template_dirs.append(settings['template_dir'])
                # if self.settings.get('template_path', ''):
                #     template_dirs.append(self.settings['template_path'])
                #byte_cache = cls.jinja2_cache()
                cache_dir = "/tmp/jinaj2_cache"
                if not os.path.exists(cache_dir):
                    os.makedirs(cache_dir)
                byte_cache = LocalFileSystemBytecodeCache(cache_dir)
                # 这个env不是全局的，那么cache有用吗？
                env = Environment(loader=FileSystemLoader(template_dirs),
                                auto_reload=False,
                                bytecode_cache=byte_cache,
                                trim_blocks=True)
                cls._template_env = env
            return cls._template_env

        @classmethod
        def jinja2_cache(cls):
            if not hasattr(cls, '_jinja2_cache'):
                cls._jinja2_cache = MemoryCache(400)
            return cls._jinja2_cache

        def render_template(self, template_name, **kwargs):
            # template_dirs = []
            # if self.settings.get('template_path', ''):
            #     template_dirs.append(self.settings['template_path'])
            # env = Environment(loader=FileSystemLoader(template_dirs))
            env = self.template_env()

            try:
                template = env.get_template(template_name)
            except TemplateNotFound:
                raise TemplateNotFound(template_name)
            with utils.util_common_loger_context(self.logger, 'template_raw_render'):
                content = template.render(kwargs)
            return content
    '''

    def _get_cache_filename(self, bucket):
        """
        使用(buket.key, bucket.checksum) 作为key的缺点，如果添加了新的url,在html中使用新的url, 通过reverse_url, 这个会导致找不到这个url,从而500
        如果使用(bucket.key) 来做为key的话, 在本地开发中，每次修改html都必须重启服务器，然后删除缓存,
            想了一下，应该只需要删除缓存就好了呀
        """
        return path.join(self.directory, "__jinja2_%s_%s.cache" % (bucket.key, bucket.checksum)
                         )

    def get_bucket(self, environment, name, filename, source):
        """Return a cache bucket for the given template.  All arguments are
        mandatory but filename may be `None`.
        """
        logging.debug("name:{}, filename:{}".format(
            name, filename
        ))
        key = self.get_cache_key(name, filename)
        checksum = self.get_source_checksum(source)
        bucket = Bucket(environment, key, checksum)
        self.load_bytecode(bucket)
        return bucket

    def get_source_checksum(self, source):
        """Returns a checksum for the source."""
        return md5(source.encode("utf-8")).hexdigest()

    def load_bytecode(self, bucket):
        logging.debug("load_bytecode {} {}, {}".format(bucket.environment, bucket.key, bucket.checksum))
        super().load_bytecode(bucket)
        # f = open_if_exists(self._get_cache_filename(bucket), "rb")
        # if f is not None:
        #     try:
        #         bucket.load_bytecode(f)
        #     finally:
        #         f.close()

    def dump_bytecode(self, bucket):
        logging.debug("dump_bytecode, {}, {}, {}".format(
            bucket.environment,
            bucket.key,
            bucket.checksum
        ))
        super().dump_bytecode(bucket)
