from pioneer.common.gui import Product

from PyQt5.QtCore import pyqtSignal, pyqtProperty, QVariant

import numpy as np

class PackageFilter(Product.VariantProduct):
    def __init__(self, parent = None):
        super(PackageFilter, self).__init__(parent)

        self._packages = None
        self._specs = None
        self._filter = {'ampMin': -2**14, 'ampMax': 2**14, 'distMin': 0, 'distMax': 300, 'rejectedFlags' : []}

    Product.InputProperty(vars(), 'QVariant', 'filter')
    Product.InputProperty(vars(), Product.VariantProduct, 'packages')

    def _update(self):
        if self._packages is not None and self._packages._variant is not None:

            data = self._packages._variant['data']

            f = (self._filter['ampMin'] <  data['amplitudes']) \
                    & (data['amplitudes'] < self._filter['ampMax']) \
                    & (self._filter['distMin'] <  data['distances']) \
                    & (data['distances'] < self._filter['distMax']) \
                    & (data['flags'] == 1) #, self._filter['rejectedFlags'], invert = True)

            self._variant = self._packages._variant.copy()
            self._variant['data'] = np.ascontiguousarray(data[f])






