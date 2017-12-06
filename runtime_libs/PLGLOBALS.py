from PLHELPER import m, extract_value, ISNULL, NULL
from PLCURSOR import PLCURSOR

class _PL_EXCEPTION(RuntimeError):
    pass

class PLGLOBALS:

    @staticmethod
    def INSTR(st, sub):
        st: str = extract_value(st)
        sub: str = extract_value(sub)
        index = st.find(sub)
        return m(index + 1)

    @staticmethod
    def MOD(n, mod):
        n = extract_value(n)
        mod = extract_value(mod)
        return m(n % mod)

    @staticmethod
    def REPLACE(char, search, replacement=None):
        if replacement is None:
            replacement = NULL()
        if ISNULL(char) or ISNULL(search):
            return char
        char: str = extract_value(char)
        search: str = extract_value(search)
        if not ISNULL(replacement):
            replacement = extract_value(replacement)
        else:
            replacement = ""
        value = char.replace(search, replacement)
        return m(value)

    class LOGIN_DENIED(_PL_EXCEPTION):
        pass

    OTHERS = _PL_EXCEPTION
    SQL = PLCURSOR
