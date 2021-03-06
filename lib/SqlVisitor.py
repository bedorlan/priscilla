import ast
import sys
from typing import List
from collections import *
from common import *
from BaseVisitor import *

sys.path.append('./built')
from PlSqlParser import PlSqlParser
from PlSqlParserVisitor import PlSqlParserVisitor

class SqlVisitor(BaseVisitor):
# pylint: disable=I0011,C0103

    def visitData_manipulation_language_statements(self, ctx: PlSqlParser.Data_manipulation_language_statementsContext):
        ret = self.visitSelect_statement(ctx)
        ret = deque(ret)
        sql: SQL = ret.popleft()
        params = [ast.Str(s=param.varname) for param in ret]
        return ast.Call(
            func=ast.Attribute(
                value=ast.Name(id=PKG_PLCURSOR),
                attr="FULL_EXECUTE"
            ),
            args=[
                ast.Str(s=sql.sql),
                ast.List(elts=params),
                ast.Call(
                    func=ast.Name(id="locals"),
                    args=[],
                    keywords=[]
                )
            ],
            keywords=[]
        )

    def visitSelect_statement(self, ctx: PlSqlParser.Select_statementContext):
        ret = self.visitChildren(ctx)
        sql = get_original_text(ctx)
        for param in ret:
            param.start_index -= ctx.start.start
            param.stop_index -= ctx.start.start
        sql = SQL(sql)
        possible_params = ret
        locals_known = self.vars_declared
        sql, params = self.bindSqlAndGetParams(sql, possible_params, locals_known)
        return [sql] + params

    def bindSqlAndGetParams(
            self,
            sql: SQL,
            possible_params: List[SQL_VAR],
            locals_known: List[str]
    ):
        """replace in the sql, the declared variables for binds"""
        unique_params = set(possible_params)
        offset = 0
        for param in possible_params:
            if param.varname in locals_known:
                param_name_id = (".").join([param.varname] + param.attrs)
                param_name_id = f':"{param_name_id}"'
                var_start = param.start_index + offset
                var_stop = param.stop_index + offset + 1
                sql.sql = sql.sql[:var_start] + param_name_id + sql.sql[var_stop:]
                offset += 3
            elif param in unique_params:
                unique_params.remove(param)
        params_found = list(unique_params)
        return sql, params_found

    def visitGeneral_element(self, ctx: PlSqlParser.General_elementContext):
        ret = self.visitChildren(ctx)
        if len(ret) <= 1:
            return ret
        if len(ret) > 2:
            # no idea what is this
            return None
        record, field = ret
        record.attrs.append(field.varname)
        record.stop_index = field.stop_index
        return record

    def visitRegular_id(self, ctx: PlSqlParser.Regular_idContext):
        if not ctx.REGULAR_ID():
            the_id = ctx.getText().upper()
        else:
            the_id = ctx.REGULAR_ID().getText().upper()
        param = SQL_VAR()
        param.varname = the_id
        param.start_index = ctx.start.start
        param.stop_index = ctx.stop.stop
        return param
