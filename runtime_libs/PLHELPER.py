
def v(value):
    if callable(value):
        return value()
    return value
