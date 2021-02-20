from django import forms


class HexColorWidget(forms.Widget):
    template_name = "morris/hex_color.html"

    class Media:
        js = [
            "morris/js/hex_color.js",
        ]
