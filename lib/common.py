import antlr4
from typing import List

class ELIF:
    pass

class ELSE:
    pass

class TYPE:
    def __init__(self, the_type):
        self.the_type = the_type

class SQL:
    def __init__(self, sql: str):
        self.sql: str = sql

class SQL_VAR:
    def __init__(self):
        self.varname: str = None
        self.attrs: List[str] = []
        self.start_index: int = None
        self.stop_index: int = None
    def __hash__(self):
        return self.varname.__hash__()
    def __eq__(self, other):
        return isinstance(other, SQL_VAR) and self.varname == other.varname

def get_spec_classname_by_classname(classname: str) -> str:
    return "_" + classname + "_spec"

def full_flat_arr(arr):
    return [elem for elem in find_elems(arr)]

def find_elems(arr):
    if arr is None:
        return
    if not isinstance(arr, list):
        yield arr
        return
    for elem in arr:
        yield from find_elems(elem)

def flat_arr(arr):
    return [find_life(elem) for elem in arr]

def find_life(arr):
    if isinstance(arr, list):
        if arr:
            return find_life(arr[0])
        return None
    else:
        return arr

def add_no_repeat(a_list: list, items):
    if not isinstance(items, list):
        items = [items]
    for item in items:
        if not item in a_list:
            a_list.append(item)

def get_original_text(ctx: antlr4.ParserRuleContext) -> str:
    return ctx.start.getInputStream().getText(ctx.start.start, ctx.stop.stop)
