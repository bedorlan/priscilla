import sys
import ast
from common import *

sys.path.append('./built')
from PlSqlParser import PlSqlParser
from PlSqlParserVisitor import PlSqlParserVisitor

class BaseVisitor(PlSqlParserVisitor):
# pylint: disable=I0011,C0103

    def __init__(self):
        self.pkgs_in_file = []
        self.pkgs_calls_found = []
        self.vars_in_package = []
        self.vars_declared = []
        self.pkg_name: str = None

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
                continue
            imports.append(ast.ImportFrom(
                module=name,
                names=[ast.alias(name="*", asname=None)],
                level=0
            ))
        return imports
