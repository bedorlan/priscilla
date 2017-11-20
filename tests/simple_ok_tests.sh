#!bash

root=$PWD
pkgsDir=$root/tests/pkgs

test_description="pkgs simple OK test"
. $root/sharness/sharness.sh

find $pkgsDir -type f | sort | while read pkg; do
  testName=$(basename $pkg .pkg)
  test_expect_success $testName '
    output=$(python3 '$root'/built/generated/'$testName'.py)
    test "$output" = "OK"
  '
done

EXIT_OK=yes
