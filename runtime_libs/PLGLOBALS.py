
class _PL_EXCEPTION(RuntimeError):
    pass

class PLGLOBALS:

    @staticmethod
    def MOD(n: int, mod: int) -> int:
        return n % mod

    class LOGIN_DENIED(_PL_EXCEPTION):
        pass

    OTHERS = _PL_EXCEPTION
