from NULL import NULL
from Mutable import extract_value, is_mutable, m, PleaseNotMutable

def ISNULL(value):
    value = extract_value(value)
    ret = isinstance(value, NULL) \
        or isinstance(value, str) and value == ""
    ret = m(ret)
    return ret

def NOT(value):
    value = extract_value(value)
    if isinstance(value, NULL) \
        or isinstance(value, str) and value == "":
        ret = NULL()
    else:
        ret = not value
    ret = m(ret)
    return ret

def CONCAT(v1, v2):
    v1 = extract_value(v1)
    v2 = extract_value(v2)
    return m(str(v1) + str(v2))

def mrange(x, y):
    x = extract_value(x)
    y = extract_value(y)
    for i in range(x, y + 1):
        yield m(i)
