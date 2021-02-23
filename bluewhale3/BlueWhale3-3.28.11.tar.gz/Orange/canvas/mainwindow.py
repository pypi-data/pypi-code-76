from AnyQt.QtCore import Qt
from AnyQt.QtWidgets import (
    QFormLayout, QCheckBox, QLineEdit, QWidget, QVBoxLayout, QLabel
)
from orangecanvas.application.settings import UserSettingsDialog, FormLayout
from orangecanvas.document.usagestatistics import UsageStatistics
from orangecanvas.utils.overlay import NotificationOverlay

from orangewidget.workflow.mainwindow import OWCanvasMainWindow

from Orange.i18n_config import *
def __(key):
    return i18n.t("orange." + key)


class OUserSettingsDialog(UserSettingsDialog):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        w = self.widget(0)  # 'General' tab
        layout = w.layout()
        assert isinstance(layout, QFormLayout)
        cb = QCheckBox(self.tr(__("checkbox.auto_update")))
        cb.setAttribute(Qt.WA_LayoutUsesWidgetRect)

        layout.addRow(__("btn.update"), cb)
        self.bind(cb, "checked", "startup/check-updates")

        # Reporting Tab
        tab = QWidget()
        self.addTab(tab, self.tr(__("btn.report")),
                    toolTip=__("btn.report_tip"))

        form = FormLayout()
        line_edit_mid = QLineEdit()
        self.bind(line_edit_mid, "text", "reporting/machine-id")
        form.addRow(__("row.machine_id"), line_edit_mid)

        box = QWidget()
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        cb1 = QCheckBox(
            self.tr(__("checkbox.share")),
            toolTip=self.tr(__("checkbox.share_tip"))
        )
        self.bind(cb1, "checked", "reporting/send-statistics")
        cb1.clicked.connect(UsageStatistics.set_enabled)
        layout.addWidget(cb1)
        box.setLayout(layout)
        form.addRow(self.tr(__("row.anonymous_statistic")), box)
        # label = QLabel(__("label.more_info"))
        # label.setOpenExternalLinks(True)
        # form.addRow(self.tr(""), label)

        tab.setLayout(form)

        # Notifications Tab
        tab = QWidget()
        self.addTab(tab, self.tr(__("btn.notification")),
                    toolTip=__("btn.notification_tip"))

        form = FormLayout()

        box = QWidget()
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        cb = QCheckBox(
            self.tr(__("checkbox.enable_notification")), self,
            toolTip=__("checkbox.enable_notification_tip")
        )
        self.bind(cb, "checked", "notifications/check-notifications")

        layout.addWidget(cb)
        box.setLayout(layout)
        form.addRow(self.tr(__("row.startup")), box)

        notifs = QWidget(self, objectName="notifications-group")
        notifs.setLayout(QVBoxLayout())
        notifs.layout().setContentsMargins(0, 0, 0, 0)

        cb1 = QCheckBox(self.tr(__("checkbox.announcement")), self,
                        toolTip=__("checkbox.announcement_tip"))

        cb2 = QCheckBox(self.tr(__("checkbox.blog_post")), self,
                        toolTip=__("checkbox.blog_post_tip"))
        cb3 = QCheckBox(self.tr(__("checkbox.new_feature")), self,
                        toolTip=__("checkbox.new_feature_tip"))

        self.bind(cb1, "checked", "notifications/announcements")
        self.bind(cb2, "checked", "notifications/blog")
        self.bind(cb3, "checked", "notifications/new-features")

        notifs.layout().addWidget(cb1)
        notifs.layout().addWidget(cb2)
        notifs.layout().addWidget(cb3)

        form.addRow(self.tr(__("row.notification_about")), notifs)
        tab.setLayout(form)


class MainWindow(OWCanvasMainWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.notification_overlay = NotificationOverlay(self.scheme_widget)
        self.notification_server = None

    def open_canvas_settings(self):
        # type: () -> None
        """Reimplemented."""
        dlg = OUserSettingsDialog(self, windowTitle=self.tr(__("menu.perferences")))
        dlg.show()
        status = dlg.exec_()
        if status == 0:
            self.user_preferences_changed_notify_all()

    def set_notification_server(self, notif_server):
        self.notification_server = notif_server

        # populate notification overlay with current notifications
        for notif in self.notification_server.getNotificationQueue():
            self.notification_overlay.addNotification(notif)

        notif_server.newNotification.connect(self.notification_overlay.addNotification)
        notif_server.nextNotification.connect(self.notification_overlay.nextWidget)

    def create_new_window(self):  # type: () -> CanvasMainWindow
        window = super().create_new_window()
        window.set_notification_server(self.notification_server)
        return window
