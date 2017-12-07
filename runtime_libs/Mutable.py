from NULL import NULL

class Mutable:
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
        other = extract_value(other)
        my_type = type(self.value)
        if my_type != NULL and not isinstance(other, my_type):
            other = my_type(other)
        return m(self.value == other)

    def __ne__(self, other):
        other = m(other)
        return m(self.value != other.value)

    def __gt__(self, other):
        other = m(other)
        return m(self.value > other.value)

    def __lt__(self, other):
        other = m(other)
        return m(self.value < other.value)

    def __ge__(self, other):
        other = m(other)
        return m(self.value >= other.value)

    def __le__(self, other):
        other = m(other)
        return m(self.value <= other.value)

    def __add__(self, other):
        other = m(other)
        return m(self.value + other.value)

    def __sub__(self, other):
        other = m(other)
        return m(self.value - other.value)

    def __mul__(self, other):
        other = m(other)
        return m(self.value * other.value)

    def __truediv__(self, other):
        other = m(other)
        return m(self.value / other.value)

    def __mod__(self, other):
        other = m(other)
        return m(self.value % other.value)

    def __ilshift__(self, other):
        if isinstance(other, PleaseNotMutable):
            return other
        other = m(other)
        self.value = other.value
        return self

class PleaseNotMutable:
    pass

def m(value=None):
    if value is None:
        value = NULL()
    elif isinstance(value, PleaseNotMutable) or is_mutable(value):
        return value
    return Mutable(value)

def is_mutable(value):
    return isinstance(value, Mutable)

def extract_value(value):
    if is_mutable(value):
        return value.value
    return value
