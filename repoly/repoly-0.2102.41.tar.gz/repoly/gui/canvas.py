from typing import TYPE_CHECKING

from PySide6.QtGui import QPainter
from PySide6.QtWidgets import QLabel

from repoly.gui.entityform import EntityForm
from repoly.gui.rectpolyform import RectPolyForm

if TYPE_CHECKING:
    from repoly.gui.window import Window


class Canvas(QLabel):
    def __init__(self, parent: "Window"):
        super().__init__()
        self.app = parent
        self.forms = []
        self.setMouseTracking(True)
        self.setFixedWidth(self.app.dimensions[0])

    def __lshift__(self, entityform: EntityForm):
        self.forms.append(entityform)

    def paintEvent(self, event):
        painter = QPainter(self)
        for form in self.forms:
            form.draw(painter)

    def mousePressEvent(self, event):
        pos = event.pos() / self.app.scale
        # Loop in reverse order, since the focus on entities is prioritary (instead of rectpoly).
        for form in reversed(self.forms):
            orientation = form.orientation_at(pos)
            if orientation:
                self._replace_form(form, orientation)
                self.update()
                return

    def _replace_form(self, form, orientation):
        updated_form = self._update_entity_form(form, orientation)
        idx = self.forms.index(form)
        self.forms[idx] = updated_form
        self.app.vlayout.replaceWidget(form, updated_form)
        form.close()

    @staticmethod
    def _update_entity_form(form, orientation):
        # Code to update other fields in future versions:
        # if isinstance(form, RectPolyForm):
        #     args = [list(form.geoobj.points.values())]
        # elif isinstance(form, EntityForm):
        #     args = form.entity.position, form.entity.relative_size
        # else:
        #     raise Exception(f"Unknown form {form}")
        # klass = form.geoobj.__class__
        # updated_geobj = klass(*args, orientation.__class__, self.app.scale)

        if isinstance(form, RectPolyForm):
            return form.replace(
                geoobj=form.geoobj.replace(orien_class=orientation.__class__)
            )
        elif isinstance(form, EntityForm):
            newentity = form.entity.update_size_for_orientation(
                orientation.__class__
            )
            return form.replace(geoobj=newentity)
        raise Exception(f"Unknown form {form}")
