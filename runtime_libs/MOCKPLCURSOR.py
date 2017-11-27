import unittest.mock as mock
from typing import List, Dict, Deque
from collections import deque
import ast
import re
import cx_Oracle

class MOCKPLCURSOR:
# pylint: disable=I0011,C0103

    class MOCKSQL:
        def __init__(self, sql: str):
            self.datasource: Deque[List] = None
            self.cursor = None
            _sqls_mocked[sql] = self

        def RETURNS(self, datasource: str):
            list_of_lists = ast.literal_eval(datasource)
            self.datasource = deque(list_of_lists)

        def EXPECT_HAVEBEENOPENWITH(self, str_params: str):
            params = ast.literal_eval(str_params)
            self.cursor.execute.assert_called_with(mock.ANY, params)

class _FakeCursor:
    def __init__(self):
        self.mocksql: MOCKPLCURSOR.MOCKSQL = None

    def execute(self, sql: str, params=None):
        if not params:
            params = {}
        for key in _sqls_mocked:
            if re.match(key, sql):
                self.mocksql = _sqls_mocked[key]
                self.mocksql.cursor = self
                return

    def fetchone(self):
        return self.mocksql.datasource.popleft()

    def close(self):
        pass

class _FakeConnection:
    def __init__(self, connection_string: str):
        pass

    def cursor(self):
        cursor = _FakeCursor()
        cursor.execute = mock.Mock(wraps=cursor.execute)
        return cursor

_sqls_mocked: Dict[str, MOCKPLCURSOR.MOCKSQL] = {}
cx_Oracle.connect = mock.Mock(side_effect=_FakeConnection)
