import unittest.mock as mock
from typing import List, Dict, Deque
from collections import deque
import ast
import re
import cx_Oracle
from PLHELPER import extract_value, PleaseNotMutable
from PLCURSOR import PLCURSOR

class MOCKPLCURSOR:
# pylint: disable=I0011,C0103

    class MOCKSQL(PleaseNotMutable):
        def __init__(self, sql):
            sql = extract_value(sql)
            self.datasource: Deque[List] = None
            self.cursor = None
            self.rowcount = None
            _sqls_mocked[sql] = self

        def RETURNS(self, datasource):
            list_of_lists = ast.literal_eval(datasource.value)
            self.datasource = deque(list_of_lists)

        def ROWCOUNT(self, rowcount):
            self.rowcount = rowcount.value

        def EXPECT_HAVEBEENOPENWITH(self, str_params):
            params = ast.literal_eval(str_params.value)
            self.cursor.execute.assert_called_with(mock.ANY, params)

    @staticmethod
    def EXPECT_COMMIT():
        PLCURSOR.conn.commit.assert_called()

    @staticmethod
    def EXPECT_ROLLBACK():
        PLCURSOR.conn.rollback.assert_called()

class _FakeCursor:
    def __init__(self, conn):
        self.conn = conn
        self.mocksql: MOCKPLCURSOR.MOCKSQL = None
        self.rowcount = None

    def execute(self, sql: str, params=None):
        sql = extract_value(sql)
        if not params:
            params = {}
        for key in _sqls_mocked:
            if not re.search(key, sql, re.IGNORECASE):
                continue
            self.mocksql = _sqls_mocked[key]
            del _sqls_mocked[key]
            self.mocksql.cursor = self
            self.rowcount = self.mocksql.rowcount
            return
        raise RuntimeError("unable to find valid sql mock")

    def fetchone(self):
        if not self.mocksql.datasource:
            return None
        return self.mocksql.datasource.popleft()

    def close(self):
        pass

class _FakeConnection:
    def __init__(self, connection_string: str):
        self.commit = mock.Mock()
        self.rollback = mock.Mock()

    def cursor(self):
        cursor = _FakeCursor(self)
        cursor.execute = mock.Mock(wraps=cursor.execute)
        return cursor

_sqls_mocked: Dict[str, MOCKPLCURSOR.MOCKSQL] = {}
cx_Oracle.connect = mock.Mock(side_effect=_FakeConnection)
