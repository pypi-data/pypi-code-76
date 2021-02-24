import io
from base64 import b64encode

from tqdm import tqdm


def get_bytes(img):
    with io.BytesIO() as output:
        img.save(output, 'jpeg')
        im_bytes = output.getvalue()
    return im_bytes


class DemoBuilder:
    def __init__(self, item_to_html, track_progress=False):
        self.track_progress = track_progress
        self.item_to_html = item_to_html
        self._init()

    def _init(self):
        self.content = ''
        self._add_head()

    def _add_head(self):
        self.content += """
                            <body>
                                <div style="width: 100%;">
                                <style>
                                .stroke {
                                  color: white;
                                  text-shadow: -1px -1px 0 #000, 1px -1px 0 #000, -1px 1px 0 #000, 1px 1px 0 #000;
                                }
                                </style>
                        """

    def add_items(self, items):
        if self.track_progress:
            items = tqdm(items)
        for item in items:
            self.add_item(item)

    def break_div(self):
        self.content += '''
                            <br style="clear:both" />
                        '''

    def add_item(self, item, *args, **kwargs):
        self.content += self.item_to_html(item, *args, **kwargs)

    def add_title(self, content):
        self.content += f'<h1 align="center"><b>{content}</b></h1>'

    def finish(self):
        self.content += """
                            </div>
                        </body>
                    </html>
                    """
        return self.content

    def save_to(self, path):
        with open(path, 'w') as f:
            f.write(self.content)

    def clear(self):
        self._init()


def image_adder(normalize=None):
    def denorm(short=False):
        if short:
            return normalize + '= "{}"' if normalize is not None else ''
        else:
            return f'{normalize}:' + '{}px' if normalize is not None else ''

    def add_image(image, name, side=300, title=None):
        if title is None:
            title = name
        return f'''
                <div style="position:relative; {denorm().format(side)}; float:left">
                    <span style="position:absolute; top:0; color:white" class="stroke">{name}</span>\n
                    <img src="data:image/png;base64,{b64encode(get_bytes(image)).decode('utf-8')}" title="{title}" {denorm(short=True).format(side)}/>\n
                </div>
               '''

    return add_image
