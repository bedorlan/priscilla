import sys
import ast
import pdb
from collections import deque

sys.path.append('./built')
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

class BaseVisitor(PlSqlParserVisitor):
# pylint: disable=I0011,C0103

    def __init__(self):
        self.pkgs_calls_found = []
        self.vars_declared = []
        self.pkg_name: str = None

    def aggregateResult(self, aggregate, nextResult):
        if aggregate is None:
            aggregate = []
        if nextResult is None:
            return aggregate
        aggregate.append(nextResult)
        return aggregate

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

    def visitStatement(self, ctx: PlSqlParser.StatementContext):
        statements = self.visitChildren(ctx)
        statement = statements[0]

        return ast.Expr(
            value=statement
        )

    def visitAssignment_statement(self, ctx: PlSqlParser.Assignment_statementContext):
        ret = self.visitChildren(ctx)
        ret = full_flat_arr(ret)
        name, value, *_ = ret + [None, None]
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

    def visitSeq_of_declare_specs(self, ctx: PlSqlParser.Seq_of_declare_specsContext):
        ret = self.visitChildren(ctx)
        ret = full_flat_arr(ret)
        self.vars_declared = [assign.targets[0].id for assign in ret]
        return ret

    def visitVariable_declaration(self, ctx: PlSqlParser.Variable_declarationContext):
        ret = self.visitChildren(ctx)
        ret = full_flat_arr(ret)
        ret = deque(ret)
        name: ast.Name = ret.popleft()
        value = ret[0] if len(ret) == 1 else ast.NameConstant(value=None)
        return ast.Assign(
            targets=[name],
            value=value
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

    def visitLogical_expression(self, ctx: PlSqlParser.Logical_expressionContext):
        ret = self.visitChildren(ctx)
        ret = full_flat_arr(ret)
        if ctx.NOT():
            return ast.UnaryOp(
                op=ast.Not(),
                operand=ret[0]
            )
        if len(ret) == 1:
            return ret
        operator = ast.And() if ctx.AND() else ast.Or()
        return ast.BoolOp(
            op=operator,
            values=ret
        )

    def visitType_declaration(self, ctx: PlSqlParser.Type_declarationContext):
        ret = self.visitChildren(ctx)
        ret = full_flat_arr(ret)
        if ctx.table_type_def():
            return ast.Assign(
                targets=ret,
                value=ast.Name(id="list")
            )
        print("unsupported")
        print(ret)
        return None

    def visitType_spec(self, ctx: PlSqlParser.Type_specContext):
        ret = self.visitChildren(ctx)
        #TODO
        return None

    def visitRelational_operator(self, ctx: PlSqlParser.Relational_operatorContext):
        text = ctx.getText()
        operator = OPERATORS[text]
        return operator()

    def visitGeneral_element(self, ctx: PlSqlParser.General_elementContext):
        ret = self.visitChildren(ctx)
        ret = full_flat_arr(ret)
        name = ret[0]
        if len(ret) == 1 and name.id in self.vars_declared:
            return ret
        ret = deque(ret)
        # if the variable is not in the declare block, should be a class variable
        if len(ret) == 1:
            ret.appendleft(self.pkg_name)
        value, attr = ret
        attr = attr.id
        return ast.Attribute(
            value=value,
            attr=attr
        )

    def visitRegular_id(self, ctx: PlSqlParser.Regular_idContext):
        the_id = ctx.REGULAR_ID().getText().upper()
        return ast.Name(id=the_id)

    def visitConstant(self, ctx: PlSqlParser.ConstantContext):
        if ctx.TRUE():
            return ast.NameConstant(value=True)
        if ctx.FALSE():
            return ast.NameConstant(value=False)
        return self.visitChildren(ctx)

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
        if arr:
            return find_life(arr[0])
        return None
    else:
        return arr

def remove_duplicates(a_list: list) -> list:
    return list(set(a_list))
