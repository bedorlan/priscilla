#!bash

root=$PWD
pkgsDir=$root/tests/pkgs

test_description="pkgs simple OK test"
#verbose="t"
. $root/sharness/sharness.sh

find $pkgsDir -type f | sort | while read pkg; do
  testName=$(basename $pkg .pkg)
  test_expect_success $testName '
    output=$(python3 '$root'/built/generated/'$testName'.py)
    status_code=$?
    test "$output" = "OK" -a "$status_code" = "0"
  '
done

EXIT_OK=yes
