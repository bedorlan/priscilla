from PLHELPER import m

class PLRECORD:
    def __init__(self):
        super().__setattr__("_dict", {})

    def __getattr__(self, key):
        if key not in self._dict:
            self._dict[key] = m()
        return self._dict[key]

    def __setattr__(self, key, value):
        self._dict[key] = value
