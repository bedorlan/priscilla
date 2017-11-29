#!bash

set -e

root=$PWD
pkgsDir=$root/tests/pkgs

find $pkgsDir -type f | sort | while read pkg; do
  testName=$(basename $pkg .pkg)
  echo "testing $testName"
  output=$(python3 $root/built/generated/$testName.py)
  test "$output" = "OK"
done

echo "everything OK"
