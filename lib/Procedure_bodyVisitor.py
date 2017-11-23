import sys
import ast
from collections import deque

sys.path.append('./built')
from PlSqlLexer import PlSqlLexer
from PlSqlParser import PlSqlParser
from PlSqlParserVisitor import PlSqlParserVisitor
from BaseVisitor import *

class Procedure_bodyVisitor(BaseVisitor):
# pylint: disable=I0011,C0103
    def __init__(self, pkg_name: str):
        super().__init__()
        self.pkg_name = pkg_name

    def visitProcedure_body(self, ctx: PlSqlParser.Procedure_bodyContext):
        ret = self.visitChildren(ctx)
        ret = full_flat_arr(ret)
        ret = deque(ret)
        name = ret.popleft()
        args = []
        while True:
            arg = ret[0]
            if not isinstance(arg, ast.arg):
                break
            args.append(arg)
            ret.popleft()
        body = ret
        args = ast.arguments(
            args=args,
            defaults=[],
            vararg=None,
            kwarg=None
        )
        return ast.FunctionDef(
            name=name.id,
            args=args,
            body=body,
            decorator_list=[ast.Name(id="staticmethod")],
            returns=None
        )
