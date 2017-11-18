set -ex

root=$PWD

. $root/lib/env.sh

pushd $root/grammars-v4/plsql/
antlr4 *.g4 -o $root/built
popd

pushd $root/built
javac *.java
popd

pushd $root
javac lib/*.java -d built
popd
