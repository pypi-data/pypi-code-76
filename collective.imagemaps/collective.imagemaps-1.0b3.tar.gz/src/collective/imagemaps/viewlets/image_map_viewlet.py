# -*- coding: utf-8 -*-

from plone.app.layout.viewlets import ViewletBase


class ImageMapViewlet(ViewletBase):
    def update(self):
        self.imagemap = getattr(self.context, "imagemap", "")

    def index(self):
        return self.imagemap or u""
