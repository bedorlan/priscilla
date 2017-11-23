import sys
import ast
from abc import ABC as Abstract, abstractmethod
from collections import deque
from pprint import pprint
from typing import List
import antlr4
import astor
import pdb

sys.path.append('./built')
from PlSqlLexer import PlSqlLexer
from PlSqlParser import PlSqlParser
from PlSqlParserVisitor import PlSqlParserVisitor
from BaseVisitor import *
from Procedure_bodyVisitor import Procedure_bodyVisitor

class TheVisitor(BaseVisitor):
# pylint: disable=I0011,C0103

    def __init__(self):
        BaseVisitor.__init__(self)
        self.pkgs_in_file: List[str] = []
        self.pkg_name: str = None

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
        ret = self.visitChildren(ctx)
        ret = full_flat_arr(ret)
        ret = deque(ret)
        name: str = ret.popleft().id
        name = get_spec_classname_by_classname(name)
        body = ret
        if len(body) == 0:
            body.append(ast.Pass())
        return ast.ClassDef(
            name=name,
            body=body,
            decorator_list=[],
            bases=[]
        )

    def visitCreate_package_body(self, ctx: PlSqlParser.Create_package_bodyContext):
        self.pkg_name = name = ctx.package_name()[0].getText().upper()
        ret = self.visitChildren(ctx)
        ret = full_flat_arr(ret)
        spec_classname = get_spec_classname_by_classname(name)
        body = ret[1:]
        self.pkgs_in_file.append(name)
        return ast.ClassDef(
            name=name,
            body=body,
            decorator_list=[],
            bases=[ast.Name(id=spec_classname)]
        )

    def visitProcedure_spec(self, ctx:PlSqlParser.Procedure_specContext):
        #return self.visitChildren(ctx)
        #TODO
        return None

    def visitProcedure_body(self, ctx: PlSqlParser.Procedure_bodyContext):
        visitor = Procedure_bodyVisitor(self.pkg_name)
        ret = ctx.accept(visitor)
        self.pkgs_calls_found += visitor.pkgs_calls_found
        self.pkgs_calls_found = remove_duplicates(self.pkgs_calls_found)
        return ret

def get_spec_classname_by_classname(classname: str) -> str:
    return "_" + classname + "_spec"

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
    #astpretty.pprint(node) # este modulo esta malo. no usar :(
    code = astor.to_source(node)

    output_filename = "built/generated/" + input_filename.split("/")[-1].split(".")[0] + ".py"
    output = open(output_filename, "w")
    output.write(code)
    output.close()

if __name__ == '__main__':
    main(sys.argv)
