from django.forms import CharField, Form

from dj_cleavejs import CleaveWidget


class TestForm(Form):
    windows_xp_serial = CharField(
        widget=CleaveWidget(blocks=[5, 5, 5, 5, 5], delimiter="-", uppercase=True)
    )
    windows_95_serial = CharField(
        widget=CleaveWidget(blocks=[3, 7], delimiter="-", numericOnly=True)
    )
