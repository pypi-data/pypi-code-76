from .qutie import QtWidgets

from .widget import BaseWidget

__all__ = ['Number']

class Number(BaseWidget):

    QtClass = QtWidgets.QDoubleSpinBox

    prefix_format = "{} "
    suffix_format = " {}"

    changed = None
    editing_finished = None

    def __init__(self, value=0, *, minimum=None, maximum=None, step=1.0,
                 decimals=0, prefix=None, suffix=None, readonly=False,
                 adaptive=False, special_value=None, changed=None,
                 editing_finished=None, **kwargs):
        super().__init__(**kwargs)
        # Properties
        self.minimum = -float('inf') if minimum is None else minimum
        self.maximum = float('inf') if maximum is None else maximum
        self.step = step
        self.decimals = decimals
        self.prefix = prefix
        self.suffix = suffix
        self.readonly = readonly
        self.adaptive = adaptive
        if special_value is not None:
            self.special_value = special_value
        self.value = value
        # Callbacks
        self.changed = changed
        self.editing_finished = editing_finished
        # Connect signals
        self.qt.valueChanged.connect(lambda value: self.emit(self.changed, value))
        self.qt.editingFinished.connect(lambda: self.emit(self.editing_finished))

    @property
    def value(self):
        return self.qt.value()

    @value.setter
    def value(self, value):
        self.qt.setValue(value)

    @property
    def minimum(self):
        return self.qt.minimum()

    @minimum.setter
    def minimum(self, value):
        self.qt.setMinimum(value)

    @property
    def maximum(self):
        return self.qt.maximum()

    @maximum.setter
    def maximum(self, value):
        self.qt.setMaximum(value)

    @property
    def step(self):
        return self.qt.singleStep()

    @step.setter
    def step(self, value):
        self.qt.setSingleStep(value)

    @property
    def decimals(self):
        return self.qt.decimals()

    @decimals.setter
    def decimals(self, value):
        self.qt.setDecimals(value)

    @property
    def prefix(self):
        return self.qt.prefix().strip()

    @prefix.setter
    def prefix(self, prefix):
        if prefix is None:
            prefix = ""
        prefix = format(prefix).strip()
        if prefix:
            prefix = self.prefix_format.format(prefix)
        self.qt.setPrefix(prefix)

    @property
    def suffix(self):
        return self.qt.suffix().strip()

    @suffix.setter
    def suffix(self, suffix):
        if suffix is None:
            suffix = ""
        suffix = format(suffix).strip()
        if suffix:
            suffix = self.suffix_format.format(suffix)
        self.qt.setSuffix(suffix)

    @property
    def readonly(self):
        return self.qt.isReadOnly()

    @readonly.setter
    def readonly(self, value):
        self.qt.setReadOnly(value)
        if value:
            self.qt.setButtonSymbols(self.qt.NoButtons)
        else:
            self.qt.setButtonSymbols(self.qt.UpDownArrows)

    @property
    def adaptive(self):
        return self.qt.stepType() == self.qt.AdaptiveDecimalStepType

    @adaptive.setter
    def adaptive(self, value):
        if value:
            self.qt.setStepType(self.qt.AdaptiveDecimalStepType)
        else:
            self.qt.setStepType(self.qt.DefaultStepType)

    @property
    def special_value(self):
        return self.qt.specialValueText()

    @special_value.setter
    def special_value(self, value):
        self.qt.setSpecialValueText(value)
