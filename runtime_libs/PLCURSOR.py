from collections import deque
from typing import List, Dict
import cx_Oracle
from PLHELPER import extract_value, m, NOT, NULL, PleaseNotMutable
from PLRECORD import PLRECORD

class _CURSOR(PleaseNotMutable):
# pylint: disable=I0011,C0103

    def __init__(self, sql: str, sql_binds: List[str], cursor_params_names: List[str]):
        self.sql = sql
        self.cursor = None
        self.found = None
        self.sql_binds = sql_binds
        self.cursor_params_names = cursor_params_names

    def __call__(self):
        return self

    def OPEN(self, cursor_params: list, the_locals: Dict):
        params = {}
        for i, param_name in enumerate(self.cursor_params_names):
            value = cursor_params[i]
            value = extract_value(value)
            params[f'"{param_name}"'] = value
        for sql_bind in self.sql_binds:
            if sql_bind in self.cursor_params_names:
                continue
            if not sql_bind in the_locals:
                raise RuntimeError(f"expected variable {sql_bind} to be defined in the locals")
            value = the_locals[sql_bind]
            value = extract_value(value)
            if not isinstance(value, PLRECORD):
                params[f'"{sql_bind}"'] = value
                continue
            for key in value.keys():
                record_bind = f"{sql_bind}.{key}"
                field = value.__getattr__(key)
                field = extract_value(field)
                params[f'"{record_bind}"'] = field
        self.cursor = PLCURSOR.getConn().cursor()
        self.cursor.execute(self.sql, params)
        PLCURSOR.rowcount = self.cursor.rowcount

    def FETCH(self, *args):
        data = self.cursor.fetchone()
        self.found = data is not None
        if not self.found:
            return
        for i, arg in enumerate(args):
            value = data[i]
            if value is None:
                value = NULL()
            arg <<= m(value)

    def CLOSE(self):
        self.cursor.close()
        self.cursor = None

    def ISOPEN(self):
        return self.cursor != None

    def FOUND(self):
        if self.found is None:
            return m(NULL())
        return m(self.found)

    def NOTFOUND(self):
        return NOT(self.FOUND())

class PLCURSOR:
# pylint: disable=I0011,C0103
    _connection_string: str = None
    _conn = deque()

    @staticmethod
    def startConnection(force=False):
        if PLCURSOR._conn and not force:
            return
        if not PLCURSOR._connection_string:
            raise RuntimeError(NO_CONNECTION_STRING)
        new_conn = cx_Oracle.connect(PLCURSOR._connection_string)
        PLCURSOR._conn.appendleft(new_conn)

    @staticmethod
    def getConn():
        PLCURSOR.startConnection()
        return PLCURSOR._conn[0]

    @staticmethod
    def SETUP(connection_string: str):
        if not isinstance(connection_string, str):
            connection_string = connection_string.value
        PLCURSOR._connection_string = connection_string
        PLCURSOR.startConnection()

    @staticmethod
    def FULL_EXECUTE(sql: str, sql_vars: List[str], the_locals: Dict):
        cursor = PLCURSOR.CURSOR(sql, sql_vars, [])
        cursor.OPEN([], the_locals)
        cursor.CLOSE()

    @staticmethod
    def AUTONOMOUS_TRANSACTION():
        PLCURSOR.startConnection(force=True)

    @staticmethod
    def commit():
        PLCURSOR.getConn().commit()
        PLCURSOR.closeLastConn()

    @staticmethod
    def rollback():
        PLCURSOR.getConn().rollback()
        PLCURSOR.closeLastConn()

    @staticmethod
    def closeLastConn():
        if len(PLCURSOR._conn) <= 1:
            return
        last_conn = PLCURSOR._conn.popleft()
        last_conn.close()

    rowcount = None

    @staticmethod
    def ISOPEN():
        return False

    @staticmethod
    def ROWCOUNT():
        return PLCURSOR.rowcount

    CURSOR = _CURSOR

def execute_immediate_into(sql, *into):
    cursor = PLCURSOR.CURSOR(sql, [], [])
    cursor.OPEN([], {})
    if into:
        cursor.FETCH(*into)
    cursor.CLOSE()

NO_CONNECTION_STRING = """
The connection string is None.
Please call PLCURSOR.SETUP("user/pass@database") first
"""
