from PLHELPER import m, extract_value

class PLRECORD:
    def __init__(self):
        super().__setattr__("_dict", {})

    def __call__(self):
        return self

    def __getattr__(self, key):
        if key not in self._dict:
            self._dict[key] = m()
        return self._dict[key]

    def __setattr__(self, key, value):
        self._dict[key] = value

    def __ilshift__(self, other):
        super().__setattr__("_dict", other._dict.copy())
        return self
