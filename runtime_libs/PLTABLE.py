from PLHELPER import m

class PLTABLE:

    def __init__(self):
        self.inner_list = []

    def __getitem__(self, index: int):
        index -= 1
        self._safe_access_index(index)
        return self.inner_list[index]

    def __setitem__(self, index: int, value):
        index -= 1
        self._safe_access_index(index)
        self.inner_list[index] = value

    def __call__(self, index: int):
        return self[index]

    def delete(self):
        self.inner_list.clear()

    def count(self):
        return len(self.inner_list)

    def last(self):
        return len(self.inner_list)

    def _safe_access_index(self, index: int):
        length = len(self.inner_list)
        if length >= index + 1:
            return
        length_missing = index + 1 - length
        while length_missing > 0:
            self.inner_list.append(m())
            length_missing -= 1
