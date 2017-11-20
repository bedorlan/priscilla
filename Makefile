root := $(PWD)
built := $(root)/built/
lib := $(root)/lib/
pkgsdir := $(root)/tests/pkgs/
pysdir := $(root)/built/generated/
testpkgs := $(shell find $(pkgsdir) -type f -name "*.pkg")
testpys := $(patsubst $(pkgsdir)%.pkg,$(pysdir)%.py,$(testpkgs))
grammars := $(root)/grammars-v4/plsql/
antlr4 := java -jar $(root)/antlr-4.7-complete.jar

.PHONY: all parser tests runtests theDirs

all: parser tests runtests

parser: theDirs $(built)/PlSqlParser.py
$(built)/PlSqlParser.py: $(grammars)/*.g4
	cd $(grammars) && $(antlr4) -Dlanguage=Python3 -no-listener -visitor *.g4 -o $(built)

tests: theDirs $(testpys)
$(testpys): $(pysdir)%.py: $(pkgsdir)%.pkg $(lib)/*.py
	python3 lib/S2S.py $<

runtests:
	bash tests/simple_ok_tests.sh

theDirs: $(built) $(pysdir)
	
%/:
	mkdir -p $@
