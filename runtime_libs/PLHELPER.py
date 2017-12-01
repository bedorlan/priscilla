
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
        return self.value

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
