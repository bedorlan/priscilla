import sys
import ast
from abc import ABC as Abstract, abstractmethod
from collections import deque
from pprint import pprint
import antlr4
import astor
import pdb

sys.path.append('./built')
from PlSqlLexer import PlSqlLexer
from PlSqlParser import PlSqlParser
from PlSqlParserVisitor import PlSqlParserVisitor

OPERATORS = {
    "=": ast.Eq,
    "!=": ast.NotEq,
    "<>": ast.NotEq,
    ">": ast.Gt,
    ">=": ast.GtE,
    "<": ast.Lt,
    "<=": ast.LtE,
    "+": ast.Add,
    "-": ast.Sub,
    "*": ast.Mult,
    "/": ast.Div
}

class TheVisitor(PlSqlParserVisitor):
# pylint: disable=I0011,C0103

    def __init__(self):
        self.pkgs_calls_found = []
        self.pkgs_in_file = []

    def aggregateResult(self, aggregate, nextResult):
        if aggregate is None:
            aggregate = []
        if nextResult is None:
            return aggregate
        aggregate.append(nextResult)
        return aggregate

    def create_imports(self):
        imports = []
        for name in self.pkgs_calls_found:
            if name in self.pkgs_in_file:
                break
            imports.append(ast.ImportFrom(
                module=name,
                names=[ast.alias(name="*", asname=None)],
                level=0
            ))
        return imports

    def visitSql_script(self, ctx: PlSqlParser.Sql_scriptContext):
        ret = self.visitChildren(ctx)
        body = full_flat_arr(ret)
        imports = self.create_imports()
        body = imports + body
        return ast.Module(
            body=body
        )

    def visitAnonymous_block(self, ctx: PlSqlParser.Anonymous_blockContext):
        ret = self.visitChildren(ctx)
        flat = full_flat_arr(ret)
        return flat

    def visitCreate_package(self, ctx: PlSqlParser.Create_packageContext):
        # TODO: for now ignoring
        return None

    def visitCreate_package_body(self, ctx: PlSqlParser.Create_package_bodyContext):
        ret = self.visitChildren(ctx)
        ret = full_flat_arr(ret)
        ret = deque(ret)
        name: ast.Name = ret.popleft()
        body = ret
        self.pkgs_in_file.append(name.id)
        return ast.ClassDef(
            name=name.id,
            body=body,
            decorator_list=[],
            bases=[]
        )

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

    def visitParameter(self, ctx: PlSqlParser.ParameterContext):
        ret = self.visitChildren(ctx)
        name, *_ = full_flat_arr(ret)
        return ast.arg(
            arg=name,
            annotation=None
        )

    def visitSeq_of_statements(self, ctx: PlSqlParser.Seq_of_statementsContext):
        ret = self.visitChildren(ctx)
        return ret

    def visitDeclare_spec(self, ctx: PlSqlParser.Declare_specContext):
        ret = self.visitChildren(ctx)
        ret = full_flat_arr(ret)
        name, value, *_ = ret + [None, None]
        if value is None:
            value = ast.NameConstant(value=None)
        return ast.Assign(
            targets=[name],
            value=value
        )

    def visitStatement(self, ctx: PlSqlParser.StatementContext):
        statements = self.visitChildren(ctx)
        statement = statements[0]

        return ast.Expr(
            value=statement
        )

    def visitAssignment_statement(self, ctx: PlSqlParser.Assignment_statementContext):
        ret = self.visitChildren(ctx)
        name, value, *_ = full_flat_arr(ret) + [None, None]
        return ast.Assign(
            targets=[name],
            value=value
        )

    def visitIf_statement(self, ctx: PlSqlParser.If_statementContext):
        ret = self.visitChildren(ctx)
        test = flat_arr(ret[0])[0]
        body_expressions = flat_arr(ret[1])
        return ast.If(
            test=test,
            body=body_expressions,
            orelse=[]
        )

    def visitFunction_call(self, ctx: PlSqlParser.Function_callContext):
        ret = self.visitChildren(ctx)
        ret = full_flat_arr(ret)
        ret = deque(ret)
        routine_name = ret.popleft()
        args = ret
        return ast.Call(
            func=routine_name,
            args=args,
            keywords=[]
        )

    def visitRoutine_name(self, ctx: PlSqlParser.Routine_nameContext):
        ret = self.visitChildren(ctx)
        pkg, method = flat_arr(ret)
        if not pkg.id in self.pkgs_calls_found:
            self.pkgs_calls_found.append(pkg.id)
        return ast.Attribute(
            value=pkg,
            attr=method
        )

    def visitConcatenation(self, ctx: PlSqlParser.ConcatenationContext):
        ret = self.visitChildren(ctx)
        operands = full_flat_arr(ret)
        if len(operands) == 2:
            left, right = operands
            operator = OPERATORS[ctx.op.text]()
            return ast.BinOp(
                left=left,
                op=operator,
                right=right
            )
        elif len(operands) == 1:
            return operands
        return ret

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
        the_id = ctx.REGULAR_ID().getText().upper()
        return ast.Name(id=the_id)

    def visitNull_statement(self, ctx: PlSqlParser.Null_statementContext):
        return ast.Pass()

    def visitNumeric(self, ctx: PlSqlParser.NumericContext):
        num = int(ctx.getText())
        return ast.Num(n=num)

    def visitQuoted_string(self, ctx: PlSqlParser.Quoted_stringContext):
        str_value = ctx.CHAR_STRING().getText()[1:-1]
        return ast.Str(str_value)

def full_flat_arr(arr):
    return [elem for elem in find_elems(arr)]

def find_elems(arr):
    if arr is None:
        return
    if not isinstance(arr, list):
        yield arr
        return
    for elem in arr:
        yield from find_elems(elem)

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

class AntlrCaseInsensitiveFileInputStream(antlr4.FileStream):

    def __init__(self, filename):
        super().__init__(filename)
        input_lower = self.strdata.upper()
        self._lookaheadData = [ord(c) for c in input_lower]

    def LA(self, offset: int):
        if offset == 0:
            return 0 # undefined
        if offset < 0:
            offset += 1 # e.g., translate LA(-1) to use offset=0
        pos = self._index + offset - 1
        if pos < 0 or pos >= self._size: # invalid
            return antlr4.Token.EOF
        return self._lookaheadData[pos]


def main(argv):

    if len(argv) == 2:
        input_filename = argv[1]
    else:
        input_filename = "./tests/pkgs/BASICS.pkg"

    input_file = AntlrCaseInsensitiveFileInputStream(input_filename)
    lexer = PlSqlLexer(input_file)
    stream = antlr4.CommonTokenStream(lexer)
    parser = PlSqlParser(stream)
    tree = parser.sql_script()
    visitor = TheVisitor()
    node = tree.accept(visitor)
    #print(ast.dump(node))
    code = astor.to_source(node)

    output_filename = "built/generated/" + input_filename.split("/")[-1].split(".")[0] + ".py"
    output = open(output_filename, "w")
    output.write(code)
    output.close()

if __name__ == '__main__':
    main(sys.argv)
