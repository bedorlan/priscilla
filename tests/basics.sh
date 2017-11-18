#!/usr/bin/env bats

@test "addition using bc" {
  result="$(let a=2+2 && echo $a)"
  [ "$result" -eq 4 ]
}
