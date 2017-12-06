from PLHELPER import m, extract_value
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

    class LOGIN_DENIED(_PL_EXCEPTION):
        pass

    OTHERS = _PL_EXCEPTION
    SQL = PLCURSOR
