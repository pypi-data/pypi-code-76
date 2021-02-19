from PySide2 import QtWidgets, QtGui, QtCore

from ciomax.sections.collapsible_section import CollapsibleSection
from ciomax.components.key_value_grp import KeyValueGrpList


class EnvironmentSection(CollapsibleSection):
    ORDER = 60

    def __init__(self, dialog):
        super(EnvironmentSection, self).__init__(dialog, "Extra Environment")

        self.component = KeyValueGrpList(
            checkbox_label="Excl", key_label="Name")
        self.content_layout.addWidget(self.component)
        self.configure_signals()

    def configure_signals(self):
        """Write to store when values change"""
        self.component.edited.connect(self.on_edited)

    def on_edited(self):
        self.dialog.store.set_extra_environment(self.component.entries())

    def get_entries(self, expander):

        return [{
            "name": x[0],
            "value": expander.evaluate(x[1]),
            "merge_policy": "exclusive" if x[2] else "append"
        } for x in self.component.entries()]

    def populate_from_store(self):
        store = self.dialog.store
        super(EnvironmentSection, self).populate_from_store(store )
        
        self.component.set_entries(store.extra_environment())

