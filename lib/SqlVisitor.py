import pdb
import ast
import sys
from common import *
from BaseVisitor import BaseVisitor

sys.path.append('./built')
from PlSqlParser import PlSqlParser
from PlSqlParserVisitor import PlSqlParserVisitor

class SqlVisitor(BaseVisitor):
# pylint: disable=I0011,C0103

    def visitSelect_statement(self, ctx: PlSqlParser.Select_statementContext):
        ret = self.visitChildren(ctx)
        ret = full_flat_arr(ret)
        sql = get_original_text(ctx)
        sql = SQL(sql)
        unique_params = set(ret)
        offset = 0
        for param in ret:
            # replace in the sql, the declared variables for binds
            if param.name.id in self.vars_declared:
                var_start = param.start_index - ctx.start.start + offset
                var_stop = param.stop_index - ctx.start.start + offset + 1
                sql.sql = sql.sql[:var_start] + f":{param.name.id}" + sql.sql[var_stop:]
                offset += 1
            elif param in unique_params:
                unique_params.remove(param)
        ret = list(unique_params)
        return [sql] + ret

    def visitRegular_id(self, ctx: PlSqlParser.Regular_idContext):
        if not ctx.REGULAR_ID():
            the_id = ctx.getText().upper()
        else:
            the_id = ctx.REGULAR_ID().getText().upper()
        param = SQL_VAR()
        param.name = ast.Name(id=the_id)
        param.start_index = ctx.start.start
        param.stop_index = ctx.stop.stop
        return param
