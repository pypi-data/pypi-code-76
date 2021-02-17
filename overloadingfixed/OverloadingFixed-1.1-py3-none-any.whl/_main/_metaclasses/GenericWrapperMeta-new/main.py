class GenericWrapperMeta(type):

    def __new__(mcs, name, bases, attrs, type_=None, base=None, simplify=False):
        cls = super().__new__(mcs, name, bases, attrs)
        if type_ is None:
            return cls
        if base is None:
            base = find_base_generic(type_)
        if simplify:
            type_ = first_origin(type_)
        cls.type = type_
        cls.base = base
        if issubclass(base, typing.Mapping):
            cls.interface = typing.Mapping
        elif issubclass(base, typing.Iterable):
            cls.interface = typing.Iterable
        else:
            cls.interface = None
        cls.derive_configuration()
        cls.complexity = type_complexity(cls)
        return cls

    def __init__(cls, *_):
        pass

    def __call__(cls, type_, base=None, simplify=False):
        return cls.__class__(cls.__name__, (), {}, type_, base, simplify)

    def __eq__(cls, other):
        if isinstance(other, GenericWrapperMeta):
            return cls.type == other.type
        elif isinstance(other, typing.GenericMeta):
            return cls.type == other
        else:
            return False

    def __hash__(cls):
        return hash(cls.type)

    def __repr__(cls):
        return repr(cls.type)

    def __instancecheck__(cls, obj):
        return cls.type.__instancecheck__(obj)

    def __subclasscheck__(cls, other):
        return cls.type.__subclasscheck__(other)

    def derive_configuration(cls):
        """
        Collect the nearest type variables and effective parameters from the type,
        its bases, and their origins as necessary.
        """
        base_params = cls.base.__parameters__
        if hasattr(cls.type, '__args__'):
            # typing as of commit abefbe4
            tvars = {p: p for p in base_params}
            types = {}
            for t in iter_generic_bases(cls.type):
                if t is cls.base:
                    type_vars = tuple(tvars[p] for p in base_params)
                    parameters = (types.get(tvar, tvar) for tvar in type_vars)
                    break
                if t.__args__:
                    for arg, tvar in zip(t.__args__, t.__origin__.__parameters__):
                        if isinstance(arg, typing.TypeVar):
                            tvars[tvar] = tvars.get(arg, arg)
                        else:
                            types[tvar] = arg
        else:
            # typing 3.5.0
            tvars = [None] * len(base_params)
            for t in iter_generic_bases(cls.type):
                for i, p in enumerate(t.__parameters__):
                    if tvars[i] is None and isinstance(p, typing.TypeVar):
                        tvars[i] = p
                if all(tvars):
                    type_vars = tvars
                    parameters = cls.type.__parameters__
                    break
        cls.type_vars = type_vars
        cls.parameters = tuple(normalize_type(p, 1) for p in parameters)
