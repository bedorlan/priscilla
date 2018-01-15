from PLHELPER import m, extract_value, NULL

class PLTABLE:

    def __init__(self, default_ctor=m):
        self.inner_list = []
        self.default_ctor = default_ctor

    def __getitem__(self, index):
        index = extract_value(index)
        index -= 1
        self._safe_access_index(index)
        return self.inner_list[index]

    def __setitem__(self, index, value):
        index = extract_value(index)
        index -= 1
        self._safe_access_index(index)
        self.inner_list[index] = value

    def __call__(self, index=None):
        if index is None:
            return self
        return self[index]

    def DELETE(self):
        self.inner_list.clear()

    def EXISTS(self, index):
        index = extract_value(index)
        index -= 1
        return index >= 0 and index < len(self.inner_list)

    def COUNT(self):
        return len(self.inner_list)

    def LAST(self):
        return len(self.inner_list)

    def FIRST(self):
        return m(1) # FIXME

    def NEXT(self, index):
        index = extract_value(index)
        if index >= len(self.inner_list):
            return NULL()
        return m(index + 1)

    def PRIOR(self, index):
        index = extract_value(index)
        if index == 1:
            return NULL()
        return m(index - 1)

    def _safe_access_index(self, index: int):
        length = len(self.inner_list)
        if length >= index + 1:
            return
        length_missing = index + 1 - length
        while length_missing > 0:
            self.inner_list.append(self.default_ctor())
            length_missing -= 1

def PLTABLE_OF(ctor):
    return lambda ctor=ctor: PLTABLE(ctor)
