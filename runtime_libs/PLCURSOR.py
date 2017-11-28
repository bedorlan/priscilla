import pdb
import cx_Oracle
from typing import List, Dict

class _CURSOR:
# pylint: disable=I0011,C0103

    def __init__(self, sql: str, sql_vars: List[str]):
        self.sql = sql
        self.cursor = None
        self.sql_vars = sql_vars

    def OPEN(self, the_locals: Dict):
        params = {}
        for sql_var in self.sql_vars:
            if sql_var in params:
                continue # priority for cursor params over locals
            if not sql_var in the_locals:
                raise RuntimeError(f"expected variable {sql_var} to be defined in the locals")
            params[sql_var] = the_locals[sql_var]
        PLCURSOR.startConnection()
        self.cursor = PLCURSOR.conn.cursor()
        self.cursor.execute(self.sql, params)

    def FETCH(self):
        return self.cursor.fetchone()

    def CLOSE(self):
        self.cursor.close()
        self.cursor = None

class PLCURSOR:
# pylint: disable=I0011,C0103
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
