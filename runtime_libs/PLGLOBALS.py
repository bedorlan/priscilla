import sys
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

    class LOGIN_DENIED(_PL_EXCEPTION):
        pass

    @staticmethod
    def LENGTH(string):
        if ISNULL(string):
            return NULL()
        string = extract_value(string)
        return len(string)

    @staticmethod
    def MOD(n, mod):
        n = extract_value(n)
        mod = extract_value(mod)
        return m(n % mod)

    @staticmethod
    def NVL(expr, replacement):
        if ISNULL(expr):
            return replacement
        return expr

    OTHERS = _PL_EXCEPTION

    @staticmethod
    def RAISE_APPLICATION_ERROR(error_number, message):
        error_number = extract_value(error_number)
        message = extract_value(message)
        message = f"ORA{error_number}: {message}"
        PLGLOBALS.SQLCODE = m(error_number)
        PLGLOBALS.SQLERRM = m(message)
        raise _PL_EXCEPTION

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

    SQL = PLCURSOR
    SQLCODE = m(0)
    SQLERRM = NULL()

    @staticmethod
    def SUBSTR(string, position, length=None):
        if ISNULL(string) or ISNULL(position):
            return NULL()
        string = extract_value(string)
        position = extract_value(position)
        length = extract_value(length)
        if position == 0:
            position = 1
        if position > 0:
            position -= 1
        if length is not None:
            value = string[position:position+length]
        else:
            value = string[position:]
        return m(value)

    @staticmethod
    def TO_CHAR(value):
        if ISNULL(value):
            return NULL()
        value = extract_value(value)
        value = str(value)
        return m(value)

    @staticmethod
    def TO_NUMBER(value):
        if ISNULL(value):
            return NULL()
        value = extract_value(value)
        value = float(value)
        if value.is_integer():
            value = int(value)
        return m(value)
