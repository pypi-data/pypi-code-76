from PyQt5.QtCore import pyqtSignal as Signal, pyqtProperty as Property, pyqtSlot as Slot, QObject, QTimer, QVariant
from PyQt5.QtQuick import QQuickItem
from PyQt5.QtQml import QJSValue

import pprint
import traceback
import types

class Setter(object):
    def __init__(self, name):
        self.property_name = name
        self.attr_name = f'_{name}'
        self.signal_name = f'{name}Changed'

    def __call__(self, target, new_val):
        new_val = cvt_if_js_value(new_val)
        if getattr(target, self.attr_name) != new_val:
            setattr(target, self.attr_name, new_val)
            getattr(target, self.signal_name).emit()

class InputSetter(Setter):
    '''
        To be used with InputProperty.
        If used, 'callback' may be
        - a member function
        - the name of a member function
        - a non-member function
        It will be called if (and only if) a new input is set.
    '''
    def __init__(self, classvars, name, callback = None):
        super(InputSetter, self).__init__(name)
        self.callback_name = None
        self.callback = None
        if callback is not None:
            if callable(callback):
                if callback.__name__ in classvars: #is member function
                    self.callback_name = callback.__name__
                else:
                    self.callback = callback
            elif isinstance(callback, str) :
                if callable(getattr(classvars, callback)):
                    self.callback_name = callback
                else:
                    raise RuntimeError(f'{callback} is not a member function')


    def __call__(self, target, new_val):
        if assign_input(target, self.property_name, new_val):
            try:

                if self.callback_name is not None: #member function
                    getattr(target, self.callback_name)() #preserves polymorphism
                elif self.callback is not None:
                    self.callback() #standalone callback function
            except:
                print(traceback.format_exc())

class Getter(object):
    def __init__(self, name):
        self.name = f'_{name}'

    def __call__(self, target):
        return getattr(target, self.name)

class QVariantGetter(Getter):
    def __init__(self, name):
        super(QVariantGetter, self).__init__(name)

    def __call__(self, target):
        return QVariant(super(QVariantGetter, self).__call__(target))

class ConstGetter(object):
    def __init__(self, value):
        self.value = value

    def __call__(self, _):
        return self.value

def select_getter(typename, name):
    if typename == QVariant:
        return QVariantGetter(name)
    return Getter(name)

def goc_member_variable(classvars, name):
    if f'_{name}' not in classvars:
        classvars[f'_{name}'] = None
def RWProperty(classvars, typename, name):
    '''
        This function adds a QProperty named 'name' to a class's vars() dictionary.
        It create the getter, setter, and signal named 'nameChanged'.

        *Important* a member variable named '_name' will be expected by the getter and setter.

        A QProperty is exposed to QML.
    '''
    goc_member_variable(classvars, name)
    notify = classvars[f'{name}Changed'] = Signal()
    classvars[f'{name}'] = Property(typename, select_getter(typename, name), Setter(name), notify = notify)

def ROProperty(classvars, typename, name):
    '''
        This function adds a QProperty named 'name' to a class's vars() dictionary.
        It creates the getter, and signal named 'nameChanged'. It also creates
        a set_name() setter outside of the Qt property system.

        *Important* a member variable named '_name' will be expected by the getter.

        A QProperty is exposed to QML.
    '''
    goc_member_variable(classvars, name)
    notify = classvars[f'{name}Changed'] = Signal()
    classvars[f'{name}'] = Property(typename, select_getter(typename, name), notify = notify)
    classvars[f'set_{name}'] = Setter(name)

def ConstProperty(classvars, typename, name):
    '''
        This function adds a QProperty named 'name' to a class's vars() dictionary.
        It create the getter.

        *Important* a member variable named '_name' will be expected by the getter.

        A QProperty is exposed to QML.
    '''
    goc_member_variable(classvars, name)
    classvars[f'{name}'] = Property(typename, select_getter(typename, name), constant = True)



def InputProperty(classvars, typename, name, callback = None):
    '''
        This function adds a QProperty named 'name' to a class's vars() dictionary.
        It create the getter, setter, and signal named 'nameChanged'.

        *Important* a member variable named '_name' will be expected by the getter and setter.

        'callback' will be called if
        (and only if) a new value is set. see InputSetter for more information on 'callback'
        A QProperty is exposed to QML.
        An InputProperty is a property that turns a product dirty when needed.
        It can be a primitive type (e.g. int, string, bool, etc) or a Product,
        or a collection containing products
    '''
    goc_member_variable(classvars, name)
    notify = classvars[f'{name}Changed'] = Signal()
    classvars[f'{name}'] = Property(typename, select_getter(typename, name), InputSetter(classvars, name, callback), notify = notify)


def Q_ENUMS_mock(classvars, enumclass): #do not use, PySide2 workaround

    values = [a for a in dir(enumclass) if not a.startswith('__') and not callable(getattr(enumclass,a))]

    for v in values:
        classvars[f'{v}'] = Property(int, ConstGetter(getattr(enumclass,v)), constant = True)



class Product(QObject):
    '''
    classdocs
    '''
    productDirty = Signal()
    productClean = Signal()

    def __init__(self, parent=None):
        super(Product, self).__init__(parent)
        '''
        Constructor
        '''
        self._dirty = False
        self._dependsOn = []
        self._dependencies = []
        self._error = None
        self._producer = None
        self._autoUpdate = False

    @Property(QObject, notify = productClean)
    def bind(self):
        return self

    def set_dirty(self, d):
        if self._dirty != d:
            self._dirty = d
            self.dirtyChanged.emit()
        if self._dirty and self._autoUpdate:
            QTimer.singleShot(0, self.update) # schedule an update as soon as we go back to event loop, but not before
    dirtyChanged = Signal()
    dirty = Property(bool, Getter('dirty'), set_dirty, dirtyChanged)

    RWProperty(vars(), bool, 'autoUpdate')

    def _update(self):
        '''
        update function to override
        '''
        pass

    @Slot()
    def update(self):

        if self.dirty:

            self._error = None

            for d in self._dependencies:
                if not d.update():
                    self._error = d._error
                    return False

            try:
                self._update()
            except Exception as e:
                self._error = e
                print(traceback.format_exc())

            self.makeClean()

        return self._error is None

    @Slot()
    def makeDirty(self):
        if not self.dirty:
            self.dirty = True
            self.productDirty.emit()

    @Slot()
    def makeClean(self):
        if self.dirty:
            self.dirty = False
            self.productClean.emit()

    def set_dependsOn(self, v):
        '''
            *Important" this property is meant to be used only from QML.
            Use add/remove_dependency() from python.
        '''
        old = self._dependsOn
        if assign_input(self, "dependsOn", v):
            for d in old:
                self.remove_dependency(d)
            for d in self._dependsOn:
                self.add_dependency(d)

    dependsOnChanged = Signal()
    dependsOn = Property(list, Getter('dependsOn'), set_dependsOn, dependsOnChanged)

    def add_dependency(self, d):
        if d is not None:
            self._dependencies.append(d)
            d.productDirty.connect(self.makeDirty)
            self.makeDirty()

    def remove_dependency(self, d):
        if d is not None:
            self._dependencies.remove(d)
            d.productDirty.disconnect(self.makeDirty)
            self.makeDirty()

    def set_producer(self, producer):
        if self._producer is not None:
            raise RuntimeError("Error: tried to call set a set_producer() twice on " + str(self) + ".")
        assert(issubclass(type(producer), Product))
        self._producer = producer
        self.add_dependency(producer)
        producer.productClean.connect(self.makeClean)


class VariantProduct(Product):
    def __init__(self, parent=None, variant=None):
        super(VariantProduct, self).__init__(parent)
        self._variant = None

        self.variant = variant #calls the setter

    InputProperty(vars(), 'QVariant', 'variant')

    @Slot(str, result = QVariant)
    def dictField(self, name):
        self.update()
        if isinstance(self._variant, dict):
            return QVariant(self._variant[name])
        
        return None


################################################################################
############# Helpers ##########################################################



def default_cmp(lhs, rhs):
    try:
        return lhs != rhs
    except:
        return True

def array_cmp(lhs, rhs):
    if lhs is not None and rhs is not None:
        return lhs.__array_interface__ != rhs.__array_interface__
    else:
        return lhs is None and rhs is None

def cvt_if_js_value(value):
    if isinstance(value, QJSValue):
        return value.toVariant()
    return value

def recurse_types(f, value):
    if isinstance(value, (list, tuple)):
        for v in value:
            recurse_types(f, v)
    elif isinstance(value, dict):
        for _, v in value.items():
            recurse_types(f, v)
    elif issubclass(type(value), Product):
            f(value)

def convert_to_dict(obj):
    dir_ = dir(obj)
    dict_ = {}
    for key in dir_:
        if not key.startswith('_') and key[0].islower():
            attr = getattr(obj, key)
            if callable(attr):
                try:
                    dict_[key] = attr()
                except:
                    pass
            else:
                dict_[key] = attr
    return dict_

def assign_input(product, property_name, value):

    value = cvt_if_js_value(value)

    compare = default_cmp

    if value is not None and hasattr(value, '__array_interface__'):
        compare = array_cmp

    variable_name = f"_{property_name}"
    assert(issubclass(type(product), Product))
    current = getattr(product, variable_name)
    try:
        rv = compare(current, value)
    except:
        print(traceback.format_exc())
        rv = True

    if  rv:
        recurse_types(product.remove_dependency, current)

        setattr(product, variable_name, value)

        recurse_types(product.add_dependency, value)

        product.makeDirty()

        signal = getattr(product, f"{property_name}Changed")
        signal.emit()
        return True
    return False

