
class PLHELPER:

    @staticmethod
    def GET_VALUE(value):
        if callable(value):
            return value()
        return value
