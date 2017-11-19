import sys
import ast
import antlr4
import codegen
import astor
from pprint import pprint
import inspect

sys.path.append('./built')
from PlSqlLexer import PlSqlLexer
from PlSqlParser import PlSqlParser
from PlSqlParserVisitor import PlSqlParserVisitor

class TheVisitor(PlSqlParserVisitor):
    '''The main visitor'''

    def __init__(self):
        pass

    def aggregateResult(self, aggregate, nextResult):
        if aggregate is None:
            aggregate = []
        if nextResult is None:
            return aggregate
        aggregate.append(nextResult)
        return aggregate

    def visitSql_script(self, ctx: PlSqlParser.Sql_scriptContext):
        ret = self.visitChildren(ctx)
        return ret

    def visitStatement(self, ctx:PlSqlParser.StatementContext):
        statements = self.visitChildren(ctx)
        statement = statements[0]
        return ast.Expr(
            value=statement
        )

    def visitFunction_call(self, ctx: PlSqlParser.Function_callContext):
        ret = self.visitChildren(ctx)
        routine_name, function_argument = flat_arr(ret)
        return ast.Call(
            func=routine_name,
            args=[function_argument],
            keywords=[]
        )

    def visitRoutine_name(self, ctx: PlSqlParser.Routine_nameContext):
        ret = self.visitChildren(ctx)
        pkg, method = flat_arr(ret)
        attr = ast.Attribute(
            value=ast.Name(id=pkg),
            attr=method
        )
        return attr

    def visitRegular_id(self, ctx: PlSqlParser.Regular_idContext):
        return ctx.REGULAR_ID().getText()

    def visitQuoted_string(self, ctx: PlSqlParser.Quoted_stringContext):
        str_value = ctx.CHAR_STRING().getText()[1:-1]
        return ast.Str(str_value)

def flat_arr(arr):
    return [find_life(elem) for elem in arr]

def find_life(arr):
    if isinstance(arr, list):
        return find_life(arr[0])
    else:
        return arr

def main(argv):
    '''the main function'''

    if len(argv) == 2:
        input_filename = argv[1]
    else:
        input_filename = "./tests/pkgs/BASICS.pkg"

    input_file = antlr4.FileStream(input_filename)
    lexer = PlSqlLexer(input_file)
    stream = antlr4.CommonTokenStream(lexer)
    parser = PlSqlParser(stream)
    tree = parser.sql_script()
    visitor = TheVisitor()
    ret = tree.accept(visitor)
    pprint(ret)
    node = find_life(ret[0])
    print(astor.to_source(node))

if __name__ == '__main__':
    main(sys.argv)
