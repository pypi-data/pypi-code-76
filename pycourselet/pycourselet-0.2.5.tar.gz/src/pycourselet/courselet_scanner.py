import logging
import os
from typing import Generator, List

from jinja2 import FileSystemLoader, Environment

from .contexts import ContextManager, PageContext, FileContext
from .tokens import *


class CourseletScanner:
    def scan_directory(self, dir_path: str) -> ContextManager:
        def key_function(key):
            i = key.find('_')
            if i >= 0:
                try:
                    key = float(key[:i])
                except Exception as ex:
                    logging.exception(ex)
            return key

        file_loader = FileSystemLoader(os.path.abspath(dir_path))
        env = Environment(loader=file_loader)
        env.trim_blocks = True
        env.lstrip_blocks = True
        env.rstrip_blocks = True

        ctx = ContextManager()

        list_dir = os.listdir(dir_path)
        sorted_list_dir = sorted(list_dir, key=key_function)
        for item_name in sorted_list_dir:
            item_path = os.path.join(dir_path, item_name)
            item_path = os.path.abspath(item_path)

            ctx.push_create(FileContext, base_file_url=item_path)

            if os.path.isfile(item_path):
                title = item_name
                i = title.find('_')
                if i >= 0:
                    title = title[i + 1:]

                i = title.rfind('.')
                if i >= 0:
                    title = title[:i]
                ctx.create_branch(PageContext, title=title)

                template = env.get_template(item_name)
                output = template.render()
                self.scan(output, ctx)

        return ctx

    def scan(self, source: str, ctx: ContextManager = ContextManager()) \
            -> ContextManager:
        tokens: List[Token] = list()
        for line in source.splitlines():
            for line_token in self._parse_line(line):
                tokens.append(line_token)

        self._walk_tokens(tokens, ctx)

        return ctx

    def _parse_line(self, line: str) -> Generator[Token, None, None]:
        # Line Tokens
        header_token = HeaderToken.parse(line)
        if header_token:
            yield header_token
            return

        # Picture Tokens
        image_token = ImageToken.parse(line)
        if image_token:
            yield image_token
            return

        # List Token
        list_token = ListToken.parse(line)
        if list_token:
            yield list_token
            return

        # Enumerate Token
        result = EnumerateToken.parse(line)
        if result:
            enumerate_token = result[0]
            line = result[1]
            yield enumerate_token

        # Table
        table_token = TableRowToken.parse(line)
        if table_token:
            yield table_token
            return

        # Control Tokens
        paragraph_token = ParagraphEndToken.parse(line)
        if paragraph_token:
            yield paragraph_token
            return

        for token in TextToken.parse(line):
            yield token

    def _walk_tokens(self, tokens: List[Token], ctx: ContextManager):

        for token in tokens:
            token.walk(ctx)

        return ctx
