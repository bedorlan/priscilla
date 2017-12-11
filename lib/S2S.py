import sys
import ast
import antlr4
import astor

sys.path.append('./built')
from PlSqlLexer import PlSqlLexer
from PlSqlParser import PlSqlParser
from PlSqlParserVisitor import PlSqlParserVisitor
from ScriptVisitor import ScriptVisitor
from AntlrCaseInsensitiveFileInputStream import AntlrCaseInsensitiveFileInputStream

def main(argv):

    input_filename = argv[1]
    output_filename = argv[2]
    input_file = AntlrCaseInsensitiveFileInputStream(input_filename)
    lexer = PlSqlLexer(input_file)
    stream = antlr4.CommonTokenStream(lexer)
    parser = PlSqlParser(stream)
    tree = parser.sql_script()
    visitor = ScriptVisitor()
    node = tree.accept(visitor)
    #print(ast.dump(node))
    #astpretty.pprint(node) # este modulo esta malo. no usar :(
    try:
        code = astor.to_source(node)
    except:
        print(ast.dump(node))
        raise

    output = open(output_filename, "w")
    output.write(code)
    output.close()

if __name__ == '__main__':
    main(sys.argv)
