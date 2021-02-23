# prepare translator for module strings
from wrap_py._transl import translator as _

from wrap_engine.sprite_type_factory import Sprite_type_factory
from wrap_engine.sprite_of_type import Sprite_of_type
from wrap_engine.sprite_text import Sprite_text

from wrap_py import wrap_base, settings

from wrap_py import _wrap_sprite_utils as wsu


class wrap_sprite():
    @classmethod
    def _register_sprite(cls, sprite):
        id = wrap_base.sprite_id_manager.add_object(sprite)
        wrap_base.world.sprite_manager.add_image_sprite(sprite)
        return id

    @classmethod
    def _prepare_sprite_type(cls, sprite_type_name):
        if wrap_base.sprite_type_manager.has_sprite_type_name(sprite_type_name):
            return

        st = Sprite_type_factory.create_sprite_type_from_file(sprite_type_name,
                                                              settings.SPRITE_TYPES_PATH, False, False)
        if not st:
            st = Sprite_type_factory.create_sprite_type_from_file(sprite_type_name,
                                                                  settings.SPRITE_TYPES_PATH_ALT, False, False)

        if not st:
            err = _("Sprite {sprite_type_name} loading failed!")
            raise Exception(err.format(sprite_type_name=str(sprite_type_name)))

        wrap_base.sprite_type_manager.add_sprite_type(st, sprite_type_name)

    @classmethod
    def remove_sprite(cls, id):
        obj = wrap_base.sprite_id_manager.remove_by_id(id)
        if obj is not None:
            wrap_base.world.sprite_manager.remove_image_sprite(obj)

    @classmethod
    def sprite_exists(cls, id):
        obj = wrap_base.sprite_id_manager.get_obj_id(id)
        return obj is not None

    @classmethod
    def add_sprite(cls, sprite_type_name, x, y, visible=True, costume=None):
        # get sprite type
        cls._prepare_sprite_type(sprite_type_name)
        sprite_type = wrap_base.sprite_type_manager.get_sprite_type_by_name(sprite_type_name)
        if not sprite_type:
            err = _("Sprite {sprite_type_name} loading failed!")
            raise Exception(err.format(sprite_type_name=str(sprite_type_name)))

        # make sprite of sprite type
        sprite = Sprite_of_type(sprite_type, x, y, costume, visible)

        return cls._register_sprite(sprite)

    @classmethod
    def add_text(cls, x, y, text, visible=True, font_name="Arial", font_size=20,
                 bold=False, italic=False, underline=False,
                 text_color=(0, 0, 0),
                 back_color=None):
        sprite = Sprite_text(x, y, visible, text, font_name, font_size, bold, italic, underline, text_color, back_color,
                             angle=90)
        return cls._register_sprite(sprite)

    @classmethod
    def get_sprite_width(cls, id):
        return wsu._get_sprite_by_id(id).get_width_pix()

    @classmethod
    def get_sprite_height(cls, id):
        return wsu._get_sprite_by_id(id).get_height_pix()

    @classmethod
    def get_sprite_size(cls, id):
        return wsu._get_sprite_by_id(id).get_size_pix()

    @classmethod
    def set_sprite_original_size(cls, id):
        wsu._get_sprite_by_id(id).set_original_size()

    @classmethod
    def change_sprite_size(cls, id, width, height):
        wsu._get_sprite_by_id(id).change_size_pix(int(width), int(height))

    @classmethod
    def change_sprite_width(cls, id, width):
        wsu._get_sprite_by_id(id).change_width_pix(width)

    @classmethod
    def change_sprite_height(cls, id, height):
        wsu._get_sprite_by_id(id).change_height_pix(height)

    @classmethod
    def change_width_proportionally(cls, id, width, from_modified=False):
        wsu._get_sprite_by_id(id).change_width_pix_proportionally(width, from_modified)

    @classmethod
    def change_height_proportionally(cls, id, height, from_modified=False):
        wsu._get_sprite_by_id(id).change_height_pix_proportionally(height, from_modified)

    @classmethod
    def get_sprite_width_proc(cls, id):
        return wsu._get_sprite_by_id(id).get_width_proc()

    @classmethod
    def get_sprite_height_proc(cls, id):
        return wsu._get_sprite_by_id(id).get_height_proc()

    @classmethod
    def get_sprite_size_proc(cls, id):
        return wsu._get_sprite_by_id(id).get_size_proc()

    @classmethod
    def change_sprite_size_proc(cls, id, width, height):
        wsu._get_sprite_by_id(id).change_size_proc(int(width), int(height))

    @classmethod
    def change_sprite_width_proc(cls, id, width):
        wsu._get_sprite_by_id(id).change_width_proc(width)

    @classmethod
    def change_sprite_height_proc(cls, id, height):
        wsu._get_sprite_by_id(id).change_height_proc(height)

    @classmethod
    def change_sprite_size_by_proc(cls, id, proc):
        wsu._get_sprite_by_id(id).change_size_by_proc(proc)

    @classmethod
    def get_sprite_flipx_reverse(cls, id):
        return wsu._get_sprite_by_id(id).get_flipx_reverse()

    @classmethod
    def get_sprite_flipy_reverse(cls, id):
        return wsu._get_sprite_by_id(id).get_flipy_reverse()

    @classmethod
    def set_sprite_flipx_reverse(cls, id, flipx):
        return wsu._get_sprite_by_id(id).set_flipx_reverse(flipx)

    @classmethod
    def set_sprite_flipy_reverse(cls, id, flipy):
        return wsu._get_sprite_by_id(id).set_flipy_reverse(flipy)

    @classmethod
    def set_sprite_angle(cls, id, angle):
        wsu._get_sprite_by_id(id).set_angle_modification(angle)

    @classmethod
    def get_sprite_angle(cls, id):
        return wsu._get_sprite_by_id(id).get_angle_modification()

    @classmethod
    def get_sprite_final_angle(cls, id):
        return wsu._get_sprite_by_id(id).get_final_angle()

    @classmethod
    def get_sprite_pos(cls, id):
        return wsu._get_sprite_by_id(id).get_sprite_pos()

    @classmethod
    def get_sprite_x(cls, id):
        return wsu._get_sprite_by_id(id).get_sprite_pos()[0]

    @classmethod
    def get_sprite_y(cls, id):
        return wsu._get_sprite_by_id(id).get_sprite_pos()[1]

    @classmethod
    def move_sprite_to(cls, id, x, y):
        return wsu._get_sprite_by_id(id).move_sprite_to(x, y)

    @classmethod
    def move_sprite_by(cls, id, dx, dy):
        wsu._get_sprite_by_id(id).move_sprite_by(dx, dy)

    @classmethod
    def get_left(cls, id):
        return wsu._get_sprite_by_id(id).get_sprite_rect().left

    @classmethod
    def get_right(cls, id):
        return wsu._get_sprite_by_id(id).get_sprite_rect().right

    @classmethod
    def get_top(cls, id):
        return wsu._get_sprite_by_id(id).get_sprite_rect().top

    @classmethod
    def get_bottom(cls, id):
        return wsu._get_sprite_by_id(id).get_sprite_rect().bottom

    @classmethod
    def get_centerx(cls, id):
        return wsu._get_sprite_by_id(id).get_sprite_rect().centerx

    @classmethod
    def get_centery(cls, id):
        return wsu._get_sprite_by_id(id).get_sprite_rect().centery

    @classmethod
    def set_left_to(cls, id, left):
        wsu._get_sprite_by_id(id).set_left_to(left)

    @classmethod
    def set_right_to(cls, id, right):
        wsu._get_sprite_by_id(id).set_right_to(right)

    @classmethod
    def set_top_to(cls, id, top):
        wsu._get_sprite_by_id(id).set_top_to(top)

    @classmethod
    def set_bottom_to(cls, id, bottom):
        wsu._get_sprite_by_id(id).set_bottom_to(bottom)

    @classmethod
    def set_centerx_to(cls, id, centerx):
        wsu._get_sprite_by_id(id).set_centerx_to(centerx)

    @classmethod
    def set_centery_to(cls, id, centery):
        wsu._get_sprite_by_id(id).set_centery_to(centery)

    @classmethod
    def is_sprite_visible(cls, id):
        return wsu._get_sprite_by_id(id).get_visible()

    @classmethod
    def show_sprite(cls, id):
        wsu._get_sprite_by_id(id).set_visible(True)

    @classmethod
    def hide_sprite(cls, id):
        wsu._get_sprite_by_id(id).set_visible(False)

    @classmethod
    def calc_point_by_angle_and_distance(cls, id, angle, distance):
        return wsu._get_sprite_by_id(id).calc_point_by_angle_and_distance(angle, distance)

    @classmethod
    def calc_angle_by_point(cls, id, point):
        return wsu._get_sprite_by_id(id).calc_angle_by_point(point)

    @classmethod
    def calc_angle_modification_by_angle(cls, id, angle_to_look_to):
        return wsu._get_sprite_by_id(id).calc_angle_modification_by_angle(angle_to_look_to)


    @classmethod
    def move_sprite_at_angle(cls, id, angle, distance):
        wsu._get_sprite_by_id(id).move_sprite_at_angle(angle, distance)

    @classmethod
    def move_sprite_to_angle(cls, id, distance):
        wsu._get_sprite_by_id(id).move_sprite_to_angle(distance)

    @classmethod
    def move_sprite_to_point(cls, id, x, y, distance):
        wsu._get_sprite_by_id(id).move_sprite_to_point([x, y], distance)

    @classmethod
    def rotate_to_angle(cls, id, angle_to_look_to):
        wsu._get_sprite_by_id(id).rotate_to_angle(angle_to_look_to)

    @classmethod
    def rotate_to_point(cls, id, x, y):
        wsu._get_sprite_by_id(id).rotate_to_point([x, y])

    @classmethod
    def sprites_collide(cls, id1, id2):
        sp1 = wsu._get_sprite_by_id(id1)
        sp2 = wsu._get_sprite_by_id(id2)
        manager = wrap_base.get_sprite_manager()
        return manager.sprites_collide(sp1, sp2)

    @classmethod
    def sprites_collide_any(cls, sprite_id, sprite_id_list):
        sprite_list = wrap_base.sprite_id_manager.get_obj_list_by_id_list(sprite_id_list)
        sprite = _get_sprite_by_id(sprite_id)

        manager = wrap_base.get_sprite_manager()
        collided_sprite = manager.sprite_collide_any(sprite, sprite_list)
        if collided_sprite is None: return None

        collided_sprite_id = wrap_base.sprite_id_manager.get_obj_id(collided_sprite)
        return collided_sprite_id

    @classmethod
    def sprites_collide_all(cls, sprite_id, sprite_id_list):
        sprite_list = wrap_base.sprite_id_manager.get_obj_list_by_id_list(sprite_id_list)
        sprite = wsu._get_sprite_by_id(sprite_id)

        manager = wrap_base.get_sprite_manager()
        collided_sprite_list = manager.sprite_collide_all(sprite, sprite_list)
        return wrap_base.sprite_id_manager.get_id_list_by_obj_list(collided_sprite_list)

    ###################################################################################
    # methods related to sprites which was created from type
    @classmethod
    def change_sprite_costume(cls, id, costume_name, save_moving_angle=False, apply_proc_size=True):
        sprite = wsu._get_sprite_by_id(id, Sprite_of_type)
        if hasattr(sprite, "set_costume"):
            sprite.set_costume(costume_name, save_moving_angle, apply_proc_size)

    @classmethod
    def set_next_costume(cls, id, save_moving_angle=False, apply_proc_size=True):
        sprite = _get_sprite_by_id(id, Sprite_of_type)
        if hasattr(sprite, "set_costume_by_offset"):
            sprite.set_costume_by_offset(1, save_moving_angle, apply_proc_size)

    @classmethod
    def set_previous_costume(cls, id, save_moving_angle=False, apply_proc_size=True):
        sprite = wsu._get_sprite_by_id(id, Sprite_of_type)
        if hasattr(sprite, "set_costume_by_offset"):
            sprite.set_costume_by_offset(-1, save_moving_angle, apply_proc_size)

    @classmethod
    def get_sprite_costume(cls, id):
        sprite = wsu._get_sprite_by_id(id, Sprite_of_type)
        if hasattr(sprite, "get_sprite_costume"):
            return sprite.get_sprite_costume()
