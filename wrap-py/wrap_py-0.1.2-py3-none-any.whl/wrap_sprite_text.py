from wrap_py import _wrap_sprite_utils as wsu
from wrap_engine.sprite_text import Sprite_text

class wrap_sprite_text():
    @classmethod
    def is_sprite_text(cls, id):
        sprite = wsu._get_sprite_by_id(id)
        return isinstance(sprite, Sprite_text)

    @classmethod
    def get_font_name(cls, id):
        sprite = wsu._get_sprite_by_id(id, Sprite_text)
        return sprite.get_font_name()

    @classmethod
    def set_font_name(cls, id, name):
        sprite = wsu._get_sprite_by_id(id, Sprite_text)
        return sprite.change_data(font_name=name)

    @classmethod
    def get_font_size(cls, id):
        sprite = wsu._get_sprite_by_id(id, Sprite_text)
        return sprite.get_font_size()

    @classmethod
    def set_font_size(cls, id, size):
        sprite = wsu._get_sprite_by_id(id, Sprite_text)
        return sprite.change_data(font_size=size)

    @classmethod
    def get_font_bold(cls, id):
        sprite = wsu._get_sprite_by_id(id, Sprite_text)
        return sprite.get_font_bold()

    @classmethod
    def set_font_bold(cls, id, bold):
        sprite = wsu._get_sprite_by_id(id, Sprite_text)
        return sprite.change_data(bold=bold)

    @classmethod
    def get_font_italic(cls, id):
        sprite = wsu._get_sprite_by_id(id, Sprite_text)
        return sprite.get_font_italic()

    @classmethod
    def set_font_italic(cls, id, italic):
        sprite = wsu._get_sprite_by_id(id, Sprite_text)
        return sprite.change_data(italic=italic)

    @classmethod
    def get_font_underline(cls, id):
        sprite = wsu._get_sprite_by_id(id, Sprite_text)
        return sprite.get_font_underline()

    @classmethod
    def set_font_underline(cls, id, underline):
        sprite = wsu._get_sprite_by_id(id, Sprite_text)
        return sprite.change_data(underline=underline)

    @classmethod
    def get_text(cls, id):
        sprite = wsu._get_sprite_by_id(id, Sprite_text)
        return sprite.get_text()

    @classmethod
    def set_text(cls, id, text):
        sprite = wsu._get_sprite_by_id(id, Sprite_text)
        return sprite.change_data(text=text)

    @classmethod
    def get_text_color(cls, id):
        sprite = wsu._get_sprite_by_id(id, Sprite_text)
        return sprite.get_text_color()

    @classmethod
    def set_text_color(cls, id, text_color):
        sprite = wsu._get_sprite_by_id(id, Sprite_text)
        return sprite.change_data(text_color=text_color)

    @classmethod
    def get_back_color(cls, id):
        sprite = wsu._get_sprite_by_id(id, Sprite_text)
        return sprite.get_back_color()

    @classmethod
    def set_back_color(cls, id, back_color):
        sprite = wsu._get_sprite_by_id(id, Sprite_text)
        return sprite.change_back_color(back_color)

    @classmethod
    def get_pos(cls, id):
        sprite = wsu._get_sprite_by_id(id, Sprite_text)
        return sprite.get_pos()

    @classmethod
    def set_pos(cls, id, pos):
        sprite = wsu._get_sprite_by_id(id, Sprite_text)
        return sprite.change_pos(pos)

    @classmethod
    def get_angle(cls, id):
        sprite = wsu._get_sprite_by_id(id, Sprite_text)
        return sprite.get_angle()

    @classmethod
    def set_angle(cls, id, pos):
        sprite = wsu._get_sprite_by_id(id, Sprite_text)
        return sprite.change_angle(pos)
