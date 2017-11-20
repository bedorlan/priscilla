
root=$PWD
export CLASSPATH="$CLASSPATH:$root/antlr-4.7-complete.jar:$root/built"
export PYTHONPATH="$root/runtime_libs"

alias antlr4='java org.antlr.v4.Tool'
alias grun='java org.antlr.v4.gui.TestRig'
