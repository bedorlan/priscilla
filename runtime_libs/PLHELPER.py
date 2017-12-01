
class NULL:
    def __call__(self):
        return self

    # TODO: empty string is null
    # def __str__(self):
    #     return self.value

    def __bool__(self):
        return False

    def __neg__(self):
        return self

    def __eq__(self, other):
        return self

    def __ne__(self, other):
        return self

    def __gt__(self, other):
        return self

    def __lt__(self, other):
        return self

    def __ge__(self, other):
        return self

    def __le__(self, other):
        return self

    def __add__(self, other):
        return self

    def __sub__(self, other):
        return self

    def __mul__(self, other):
        return self

    def __truediv__(self, other):
        return self

def ISNULL(value):
    if isinstance(value, _Mutable):
        value = value.value
    ret = isinstance(value, NULL) \
        or isinstance(value, str) and value == ""
    ret = m(ret)
    return ret

def NOT(value):
    if isinstance(value, _Mutable):
        value = value.value
    if isinstance(value, NULL) \
        or isinstance(value, str) and value == "":
        ret = NULL()
    else:
        ret = not value
    ret = m(ret)
    return ret

class _Mutable:
    def __init__(self, value):
        self.value: object = value

    def __call__(self):
        return self

    def __str__(self):
        return self.value

    def __index__(self):
        return self.value

    def __hash__(self):
        return self.value.__hash__()

    def __bool__(self):
        return self.value.__bool__()

    def __neg__(self):
        return m(-(self.value))

    def __eq__(self, other):
        if not isinstance(other, _Mutable):
            other = m(other)
        return m(self.value == other.value)

    def __ne__(self, other):
        if not isinstance(other, _Mutable):
            other = m(other)
        return m(self.value != other.value)

    def __gt__(self, other):
        if not isinstance(other, _Mutable):
            other = m(other)
        return m(self.value > other.value)

    def __lt__(self, other):
        if not isinstance(other, _Mutable):
            other = m(other)
        return m(self.value < other.value)

    def __ge__(self, other):
        if not isinstance(other, _Mutable):
            other = m(other)
        return m(self.value >= other.value)

    def __le__(self, other):
        if not isinstance(other, _Mutable):
            other = m(other)
        return m(self.value <= other.value)

    def __add__(self, other):
        if not isinstance(other, _Mutable):
            other = m(other)
        return m(self.value + other.value)

    def __sub__(self, other):
        if not isinstance(other, _Mutable):
            other = m(other)
        return m(self.value - other.value)

    def __mul__(self, other):
        if not isinstance(other, _Mutable):
            other = m(other)
        return m(self.value * other.value)

    def __truediv__(self, other):
        if not isinstance(other, _Mutable):
            other = m(other)
        return m(self.value / other.value)

    def __mod__(self, other):
        if not isinstance(other, _Mutable):
            other = m(other)
        return m(self.value % other.value)

    def __ilshift__(self, other):
        if isinstance(other, PleaseNotMutable):
            return other
        if not isinstance(other, _Mutable):
            other = m(other)
        self.value = other.value
        return self

def m(value=None):
    if isinstance(value, PleaseNotMutable):
        return value
    return _Mutable(value)

class PleaseNotMutable:
    pass

def mrange(i, j):
    for i in range(i, j):
        yield m(i)
