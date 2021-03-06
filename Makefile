root := $(PWD)
built := $(root)/built/
lib := $(root)/lib/
grammars := $(root)/grammars-v4/plsql/
antlr4 := java -jar $(root)/antlr-4.7-complete.jar
export CLASSPATH := $(root)/antlr-4.7-complete.jar:$(root)/built
export PYTHONPATH := $(root)/runtime_libs
pkgsdir := $(root)/input/
pysdir := $(root)/output/
pkgs := $(shell find $(pkgsdir) -type f -name "*.pkg")
pys := $(patsubst $(pkgsdir)%.pkg,$(pysdir)%.py,$(pkgs))
testpkgsdir := $(root)/tests/pkgs/
testpysdir := $(root)/built/generated/
testpkgs := $(shell find $(testpkgsdir) -type f -name "*.pkg")
testpys := $(patsubst $(testpkgsdir)%.pkg,$(testpysdir)%.py,$(testpkgs))
dirs := $(built) $(testpysdir) $(pkgsdir) $(pysdir)
pipmodules := setuptools wheel coverage codecov antlr4-python3-runtime astor cx-Oracle
modules-installed := $(pysdir)/.modules-installed

ifndef fast
s2s := python3 -m coverage run lib/S2S.py
else
s2s := python3 lib/S2S.py
endif

.PHONY: all build buildtests test theDirs gen-grun migrate coverage coverage-html codecov
all: build buildtests test

build: theDirs $(built)/PlSqlParser.py $(modules-installed)
$(built)/PlSqlParser.py: $(grammars)/*.g4
	cd $(grammars) && $(antlr4) -Dlanguage=Python3 -no-listener -visitor *.g4 -o $(built)

buildtests: theDirs $(testpys) $(modules-installed)
$(testpys): $(testpysdir)%.py: $(testpkgsdir)%.pkg $(built)/PlSqlParser.py $(lib)/*.py
	$(s2s) $< $@

$(modules-installed):
	for module in $(pipmodules); do pip3 install $$module; done
	touch $@

test: buildtests
	bash tests/simple_ok_tests.sh

coverage:
	python3 -m coverage combine || true

coverage-html: coverage
	python3 -m coverage html

codecov: coverage
	python3 -m codecov

theDirs: $(dirs)
$(dirs):
	mkdir -p $@

migrate: $(pys)
$(pys): $(pysdir)%.py: $(pkgsdir)%.pkg
	python3 lib/S2S.py $< $@

gen-grun: $(built)/PlSqlParser.class
$(built)/PlSqlParser.class: $(grammars)/*.g4
	cd $(grammars) && $(antlr4) -no-listener *.g4 -o $(built)
	cd $(built) && javac *.java
