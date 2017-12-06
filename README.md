# priscilla
[![Build Status](https://travis-ci.org/bedorlan/priscilla.svg?branch=master)](https://travis-ci.org/bedorlan/priscilla)

PL/SQL to Python transcompiler

```
$ git clone --recursive https://github.com/bedorlan/priscilla
$ cd priscilla
$ make build
$ cat <<EOF > input/example.pkg
begin
  dbms_output.put_line('Hello');
end;
/
EOF
$ make migrate
$ export PYTHONPATH=$PWD/runtime_libs/
$ python3 output/example.py
Hello
```

This is a development version. If something doesn't work, please [let me know](https://github.com/bedorlan/priscilla/issues/new)

## Requirements
- make
- java 8
- python >= 3.6
- pip

## What is supported?
Please check the [tests](https://github.com/bedorlan/priscilla/tree/master/tests/pkgs) to see the scope

## What is not supported?
- GOTO
- Context switch. SQL invoking PL/SQL

## Roadmap
By demand