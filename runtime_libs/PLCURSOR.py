import cx_Oracle

class _CURSOR:
    def __init__(self, sql: str):
        self.sql = sql
        self.cursor = None

    def OPEN(self):
        PLCURSOR.startConnection()
        self.cursor = PLCURSOR.conn.cursor()
        self.cursor.execute(self.sql)

    def FETCH(self):
        return self.cursor.fetchone()

    def CLOSE(self):
        self.cursor.close()
        self.cursor = None

class PLCURSOR:

    _connection_string: str = None
    conn = None

    @staticmethod
    def SETUP(connection_string: str):
        PLCURSOR._connection_string = connection_string

    @staticmethod
    def startConnection():
        if PLCURSOR.conn:
            return
        if not PLCURSOR._connection_string:
            raise RuntimeError(NO_CONNECTION_STRING)
        PLCURSOR.conn = cx_Oracle.connect(PLCURSOR._connection_string)

    CURSOR = _CURSOR

NO_CONNECTION_STRING = """
The connection string is None.
Please call PLCURSOR.SETUP("user/pass@database") first
"""
