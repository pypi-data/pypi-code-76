import os
import gazu

from kabaret import flow
from kabaret.flow_contextual_dict import ContextualView, get_contextual_dict

from libreflow import baseflow

class Department(baseflow.departments.Department):
    _short_name = flow.Param(None)
    _file_prefix = flow.Computed(cached=True)
    
    def compute_child_value(self, child_value):
        if child_value is self.path:
            settings = get_contextual_dict(self, "settings")
            path = os.path.join(
                settings["film"],
                settings["sequence"],
                settings["shot"],
                settings["department"],
            )
            child_value.set(path)
        elif child_value is self._file_prefix:
            settings = get_contextual_dict(self, "settings")
            child_value.set("{film}_{sequence}_{shot}_{dept}_".format(**settings))
    
    def get_default_contextual_edits(self, context_name):
        if context_name == "settings":
            return dict(
                department=self.name(),
                dept=self._short_name.get() if self._short_name.get() else self.name(),
                context=self._parent.__class__.__name__.lower(),
            )

class LayoutDepartment(Department):
    _short_name = flow.Param("lay")

class AnimationDepartment(Department):
    _short_name = flow.Param("ani")

class MiscDepartment(Department):
    _short_name = flow.Param("misc")

class ShotDepartments(flow.Object):
    layout = flow.Child(LayoutDepartment).ui(expanded=False)
    animation = flow.Child(AnimationDepartment).ui(expanded=False)
    misc = flow.Child(MiscDepartment).ui(expanded=False)


class Shot(baseflow.film.Shot):

    _film = flow.Parent(4)
    departments = flow.Child(ShotDepartments).ui(expanded=True)

    def compute_child_value(self, child_value):
        if child_value is self.kitsu_url:
            child_value.set(
                "%s/%s" % (self._film.kitsu_url.get(), self.kitsu_id.get())
            )


class Shots(baseflow.film.Shots):

    create_shot = flow.Child(baseflow.maputils.SimpleCreateAction)

    @classmethod
    def mapped_type(cls):
        return Shot


class Sequence(baseflow.film.Sequence):

    _film = flow.Parent(2)
    shots = flow.Child(Shots).ui(default_height=420, expanded=True)

    def compute_child_value(self, child_value):
        if child_value is self.kitsu_url:
            child_value.set(
                "%s/shots?search=%s" % (self._film.kitsu_url.get(), self.name())
            )


class Sequences(baseflow.film.Sequences):

    ICON = ("icons.flow", "sequence")

    _film = flow.Parent()

    create_sequence = flow.Child(baseflow.maputils.SimpleCreateAction)
    update_kitsu_settings = flow.Child(baseflow.film.UpdateItemsKitsuSettings)

    @classmethod
    def mapped_type(cls):
        return Sequence

    def get_default_contextual_edits(self, context_name):
        if context_name == "settings":
            return self._film.get_default_contextual_edits(context_name)



class Film(flow.Object):

    ICON = ("icons.flow", "film")

    sequences = flow.Child(Sequences).ui(default_height=420, expanded=True)
    
    def get_default_contextual_edits(self, context_name):
        if context_name == "settings":
            return dict(film=self.name())


class Films(flow.Map):

    ICON = ("icons.flow", "film")

    create_film = flow.Child(baseflow.maputils.SimpleCreateAction)

    @classmethod
    def mapped_type(cls):
        return Film

    def get_default_contextual_edits(self, context_name):
        if context_name == "settings":
            return dict(file_category="PROD")


# TODO

# file_category a corriger