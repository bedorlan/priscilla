import sys
import ast
from abc import ABC as Abstract, abstractmethod
from pprint import pprint
import antlr4
import astor
import pdb

sys.path.append('./built')
from PlSqlLexer import PlSqlLexer
from PlSqlParser import PlSqlParser
from PlSqlParserVisitor import PlSqlParserVisitor
from BaseVisitor import BaseVisitor
from AntlrCaseInsensitiveFileInputStream import AntlrCaseInsensitiveFileInputStream

def main(argv):

    input_filename = argv[1]
    input_file = AntlrCaseInsensitiveFileInputStream(input_filename)
    lexer = PlSqlLexer(input_file)
    stream = antlr4.CommonTokenStream(lexer)
    parser = PlSqlParser(stream)
    tree = parser.sql_script()
    visitor = BaseVisitor()
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
