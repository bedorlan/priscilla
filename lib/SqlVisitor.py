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
        return [sql] + ret

    def visitRegular_id(self, ctx: PlSqlParser.Regular_idContext):
        if not ctx.REGULAR_ID():
            the_id = ctx.getText().upper()
        else:
            the_id = ctx.REGULAR_ID().getText().upper()
        return ast.Name(id=the_id)
