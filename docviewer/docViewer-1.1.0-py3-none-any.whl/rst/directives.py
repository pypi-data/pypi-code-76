from base64 import b64encode

from docutils.parsers.rst.directives.images import Image

from .. import plantuml


class BaseGraph(Image):
    required_arguments = 0
    optional_arguments = 1
    option_spec = Image.option_spec.copy()
    has_content = True

    def render_to_base64(self):
        output, ext = self.render_content()
        image_format = ext.lstrip('.')
        if image_format == 'svg':
            base64_format = 'svg+xml'
        else:
            base64_format = image_format
        content = f'data:image/{base64_format};base64,' \
            + b64encode(output).decode('ascii')
        return content

    def render_content(self):
        raise NotImplementedError()

    def run(self):
        self.options['alt'] = '\n'.join(self.content)
        self.arguments = [self.render_to_base64()]
        return super().run()


class PlantUML(BaseGraph):
    LSTRIP = '@startuml'
    RSTRIP = '@enduml'

    def render_content(self):
        if not self.content:
            raise ValueError('value expected')
        content = '\n'.join(self.content)
        content = content.strip()
        if content.startswith(self.LSTRIP):
            content = content[len(self.LSTRIP)]
        if content.endswith(self.RSTRIP):
            content = content[:len(self.RSTRIP)]
        output, ext = plantuml.render(content)
        return output, ext


class Uml(PlantUML):
    pass


class Graph(PlantUML):
    pass
