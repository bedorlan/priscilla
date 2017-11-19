root=$(PWD)
built=$(root)/built
lib=$(root)/lib
grammars=$(root)/grammars-v4/plsql/
antlr4=java -jar $(root)/antlr-4.7-complete.jar

all: $(built)/PlSqlParser.py

$(built)/PlSqlParser.py: $(grammars)/*.g4
	cd $(grammars) && $(antlr4) -Dlanguage=Python3 -no-listener -visitor *.g4 -o $(built)
