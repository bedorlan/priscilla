import sys
import ast
import inspect
import astpretty

if __name__ == '__main__':
    tree = ast.parse(sys.argv[1])
    astpretty.pprint(tree)
