root := $(PWD)
built := $(root)/built/
lib := $(root)/lib/
grammars := $(root)/grammars-v4/plsql/
antlr4 := java -jar $(root)/antlr-4.7-complete.jar
export CLASSPATH := $(root)/antlr-4.7-complete.jar:$(root)/built
export PYTHONPATH := $(root)/runtime_libs

pkgsdir := $(root)/input
pysdir := $(root)/output
pkgs := $(shell find $(pkgsdir) -type f -name "*.pkg")
pys := $(patsubst $(pkgsdir)%.pkg,$(pysdir)%.py,$(pkgs))

testpkgsdir := $(root)/tests/pkgs/
testpysdir := $(root)/built/generated/
testpkgs := $(shell find $(testpkgsdir) -type f -name "*.pkg")
testpys := $(patsubst $(testpkgsdir)%.pkg,$(testpysdir)%.py,$(testpkgs))

.PHONY: all build buildtests test theDirs gen-grun migrate
all: build buildtests test

build: theDirs $(built)/PlSqlParser.py
$(built)/PlSqlParser.py: $(grammars)/*.g4
	cd $(grammars) && $(antlr4) -Dlanguage=Python3 -no-listener -visitor *.g4 -o $(built)

buildtests: theDirs $(testpys)
$(testpys): $(testpysdir)%.py: $(testpkgsdir)%.pkg $(built)/PlSqlParser.py $(lib)/*.py
	python3 lib/S2S.py $< $@

test: buildtests
	bash tests/simple_ok_tests.sh

theDirs: $(built) $(testpysdir) $(pkgsdir) $(pysdir)
	
%/:
	mkdir -p $@

migrate: $(pys)
$(pys): $(pysdir)%.py: $(pkgsdir)%.pkg
	python3 lib/S2S.py $< $@

gen-grun: $(built)/PlSqlParser.class
$(built)/PlSqlParser.class: $(grammars)/*.g4
	cd $(grammars) && $(antlr4) -no-listener *.g4 -o $(built)
	cd $(built) && javac *.java
