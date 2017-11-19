root=$(PWD)
built=$(root)/built
grammars=$(root)/grammars-v4/plsql/

all: $(built)/PlSqlParser.class $(built)/S2S.class

$(built)/PlSqlParser.class: $(built)/PlSqlParser.java
	cd $(built) && javac *.java

$(built)/PlSqlParser.java:
	cd $(grammars) && antlr4 -no-listener -visitor *.g4 -o $(built)

$(built)/S2S.class: $(root)/lib/*.java
	cd lib && javac *.java -d $(built)
