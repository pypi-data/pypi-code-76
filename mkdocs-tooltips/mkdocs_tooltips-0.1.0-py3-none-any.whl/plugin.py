import re
from mkdocs.plugins import BasePlugin

class Tooltips(BasePlugin):

    @staticmethod
    def tooltip_replace(match):
        body = match.group(1)
        if match.group(0)[0] == '\\':
            return match.group(0)[1:]

        tooltip = match.group(2).split('|')[0]
        options = match.group(2).split('|')[1:]
        args = {'position': 'top'}

        for option in options:
            if option in ['top-left', 'top', 'top-right', 'right',
                          'bottom-right', 'bottom', 'bottom-left', 'left']:
                args['position'] = option
            if option in ['error', 'warning', 'info', 'success']:
                args['color'] = option
            if option in ['small', 'medium', 'large']:
                args['size'] = option
            if option in ['always', 'no-animate', 'bounce']:
                args['anim'] = option
            if option == 'rounded':
                args['style'] = 'rounded'

        span_class = ' '.join(['hint--' + arg for arg in args.values()])
        return '<span class="tooltip %s" aria-label="%s">%s</span>' \
               % (span_class, tooltip, body)

    # <pre> section displays the html code
    def on_page_markdown(self, markdown, **kwargs):
        return re.sub(r'\\?\[(.*?)\]\{(.*?)\}', self.tooltip_replace, markdown)

    # tooltip appears in <pre> section instead of tooltip markdown code
    # def on_post_page(self, output, page, config):
    #     return re.sub(r'\[(.*?)\]\{(.*?)\}', self.tooltip_replace, output)

    # tooltip appears in <pre> section instead of tooltip markdown code
    # def on_page_content(self, html, page, config, files):
    #     return re.sub(r'\[(.*?)\]\{(.*?)\}', self.tooltip_replace, html)

    # the tooltip is not created, leaving the tooltip markdown code as is
    # def on_post_template(self, output_content, template_name, config):
    #     return re.sub(r'\[(.*?)\]\{(.*?)\}', self.tooltip_replace, output_content)
