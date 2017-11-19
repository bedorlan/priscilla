root=$(PWD)
built=$(root)/built
lib=$(root)/lib
grammars=$(root)/grammars-v4/plsql/
antlr4=java -jar $(root)/antlr-4.7-complete.jar

all: $(built)/plsql_parser.go $(built)/S2S

$(built)/plsql_parser.go: $(grammars)/*.g4
	cd $(grammars) && $(antlr4) -Dlanguage=Go -no-listener -visitor *.g4 -o $(built)

$(built)/S2S: $(lib)/*.go
	cd lib && go build -o $@
