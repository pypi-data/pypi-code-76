class obj_dict(dict):
    """Adv dict class to enable sub-key

    Init Arguments:
        *args {tuple} -- key = value
        or
        **kwargs {dict} -- {key: value}
    """

    def __init__(self, *args, **kwargs):
        self.__setitem__(*args, **kwargs)

    def __split(self, key: str) -> dict:
        """Private function for split key to parent-child

        Arguments:
            key {str} -- key of dict

        Returns:
            dict -- dict return
        """
        o = key.split(".")
        rtn = {}
        if len(o) == 1:
            rtn = {"org": key, "key": o[0]}
        else:
            rtn = {"org": key, "key": ".".join(o[1:]), "par": o[0]}
        return rtn

    def __setattr__(self, *args, **kwargs):
        self.__setitem__(*args, **kwargs)

    def __getattr__(self, *args, **kwargs):
        return self.get(*args, **kwargs)

    def __setitem__(self, *args, **kwargs):
        if args == () and kwargs == {}:
            return
        if args != ():
            try:
                (k, v) = args
                kwargs.update({k: v})
            except:
                kwargs.update(args[0])
        for k, v in kwargs.items():
            o = self.__split(k)
            if o.get("par", None) == None:
                self.update({o.get("org"): v})
            else:
                par = self.get(o.get("par"), None)
                if par == None:
                    nobj = obj_dict()
                    nobj[o.get("key")] = v
                    self.update({o.get("par"): nobj})
                else:
                    if isinstance(par, obj_dict):
                        self.get(o.get("par"), None).update({o.get("key"): v})
                    else:
                        continue
