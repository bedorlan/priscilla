#!bash

set -e

root=$PWD
pkgsDir=$root/tests/pkgs

if test -n "$fast"; then
  python3="python3"
else
  python3="python3 -m coverage run"  
fi

find $pkgsDir -type f | sort | while read pkg; do
  testName=$(basename $pkg .pkg)
  echo "testing $testName"
  output=$($python3 $root/built/generated/$testName.py)
  test "$output" = "OK"
done

echo "everything OK"
