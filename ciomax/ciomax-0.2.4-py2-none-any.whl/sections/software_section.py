from PySide2 import QtWidgets, QtGui

from ciomax.sections.collapsible_section import CollapsibleSection
from ciomax.components.combo_box_grp import ComboBoxGrp
from ciocore import data as coredata
from ciocore.package_environment import PackageEnvironment
from ciomax.const import MAYA_BASE_VERSION

AVAILABLE_RENDERERS = ("{}/arnold-maya".format(MAYA_BASE_VERSION),"v-ray-standalone")

class SoftwareSection(CollapsibleSection):
    ORDER = 20

    def __init__(self, dialog):

        super(SoftwareSection, self).__init__(dialog, "Software")

        self.full_paths =  []
        self.component = ComboBoxGrp(label="Renderer")

        self.content_layout.addWidget(self.component)
        self.configure_combo_boxes()

        # Write to store when values change
        self.component.combobox.currentTextChanged.connect(
            self.on_change)

    def on_change(self, value):
        full_path = self.get_full_path(self.component.combobox.currentText())
        self.dialog.store.set_renderer_version(full_path)
 
    def populate_from_store(self):
        store = self.dialog.store
        super(SoftwareSection, self).populate_from_store(store)
        full_renderer_version = store.renderer_version()
        partial_renderer_version = full_renderer_version.split("/")[-1]

        self.component.set_by_text(partial_renderer_version)


    def configure_combo_boxes(self):
        if not coredata.valid():
            print "Invalid packages data"
            return False

        software_data = coredata.data()["software"]
        self.full_paths = sorted([p for p in software_data.to_path_list() if p.startswith(AVAILABLE_RENDERERS)])

        model = QtGui.QStandardItemModel()
        for path in self.full_paths or []:
            model.appendRow(QtGui.QStandardItem(path.split("/")[-1]))
        self.component.set_model(model)
        return True

    def resolve(self, expander, **kwargs):
        extra_environment = self.dialog.main_tab.section(
            "EnvironmentSection").get_entries(expander)

        packages_data = self.get_packages()
        if not packages_data:
            return []

        # Turn path helper off for Vray. If Arnold needs it, it can opt in using
        # extra_environment.
        packages_data["env"].extend(
            [{
                "name": "CONDUCTOR_PATHHELPER",
                "value": "0",
                "merge_policy": "exclusive",
            }]
        )

        packages_data["env"].extend(extra_environment)
        return {
            "environment": dict(packages_data["env"]),
            "software_package_ids": packages_data["ids"]
        }

    def get_packages(self):
        if not coredata.valid():
            return
        tree_data = coredata.data()["software"]
        full_path = self.get_full_path(self.component.combobox.currentText())
        package = tree_data.find_by_path(full_path)

        result = {
            "ids": [],
            "env": PackageEnvironment()
        }

        result["ids"].append(package["package_id"])
        result["env"].extend(package)
 
        return result

    def get_full_path(self, partial_path):
        return next((p for p in self.full_paths if p.endswith(partial_path)), None)

