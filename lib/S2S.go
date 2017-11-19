package main

import (
	"fmt"
	"os"

	"../built"
	"github.com/antlr/antlr4/runtime/Go/antlr"
)

type TheVisitor struct {
	parser.BasePlSqlParserVisitor
}

func (TheVisitor) VisitSql_script(ctx *parser.Sql_scriptContext) {
	fmt.Println("uuyyy")
}

func main() {
	pkgName := os.Args[1]
	input, _ := antlr.NewFileStream(pkgName)
	lexer := parser.NewPlSqlLexer(input)
	tokens := antlr.NewCommonTokenStream(lexer, 0)
	theParser := parser.NewPlSqlParser(tokens)
	tree := theParser.Sql_script()
	visitor := new(TheVisitor)
	visitor.SetSuper(visitor)
	tree.Accept(visitor)
}
