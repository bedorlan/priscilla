import sys
import ast
import antlr4
import astor
from pprint import pprint
import inspect

sys.path.append('./built')
from PlSqlLexer import PlSqlLexer
from PlSqlParser import PlSqlParser
from PlSqlParserVisitor import PlSqlParserVisitor

OPERATORS = {
    "=": ast.Eq
}

class TheVisitor(PlSqlParserVisitor):
    '''The main visitor'''

    def __init__(self):
        self.pkgs_found = []

    def aggregateResult(self, aggregate, nextResult):
        if aggregate is None:
            aggregate = []
        if nextResult is None:
            return aggregate
        aggregate.append(nextResult)
        return aggregate

    def visitSql_script(self, ctx: PlSqlParser.Sql_scriptContext):
        ret = self.visitChildren(ctx)
        statements = flat_arr(ret)
        the_import = create_import(self.pkgs_found)
        body = [the_import] + statements
        return ast.Module(
            body=body
        )

    def visitStatement(self, ctx:PlSqlParser.StatementContext):
        statements = self.visitChildren(ctx)
        statement = statements[0]
        return ast.Expr(
            value=statement
        )

    def visitIf_statement(self, ctx: PlSqlParser.If_statementContext):
        ret = self.visitChildren(ctx)
        test, body = flat_arr(ret)
        return ast.If(
            test=test,
            body=[body],
            orelse=[]
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
        if not pkg in self.pkgs_found:
            self.pkgs_found.append(pkg)
        return ast.Attribute(
            value=ast.Name(id=pkg),
            attr=method
        )

    def visitRelational_expression(self, ctx: PlSqlParser.Relational_expressionContext):
        ret = self.visitChildren(ctx)
        expr = flat_arr(ret)
        if len(expr) == 3:
            left, operator, right = expr
            return ast.Compare(
                left=left,
                ops=[operator],
                comparators=[right]
            )
        return expr[0]

    def visitRelational_operator(self, ctx: PlSqlParser.Relational_operatorContext):
        text = ctx.getText()
        operator = OPERATORS[text]
        return operator()

    def visitRegular_id(self, ctx: PlSqlParser.Regular_idContext):
        return ctx.REGULAR_ID().getText()

    def visitNumeric(self, ctx: PlSqlParser.NumericContext):
        n = ctx.getText()
        return ast.Num(n=n)

    def visitQuoted_string(self, ctx: PlSqlParser.Quoted_stringContext):
        str_value = ctx.CHAR_STRING().getText()[1:-1]
        return ast.Str(str_value)

def flat_arr(arr):
    return [find_life(elem) for elem in arr]

def find_life(arr):
    if isinstance(arr, list):
        if len(arr) > 0:
            return find_life(arr[0])
        else:
            return None
    else:
        return arr

def create_import(imports):
    aliases = [ast.alias(name=name, asname=None) for name in imports]
    return ast.Import(names=aliases)

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
    node = tree.accept(visitor)
    pprint(node, sys.stderr)
    code = astor.to_source(node)

    output_filename = "built/generated/" + input_filename.split("/")[-1].split(".")[0] + ".py"
    output = open(output_filename, "w")
    output.write(code)
    output.close()

if __name__ == '__main__':
    main(sys.argv)
