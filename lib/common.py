import antlr4

class ELIF:
    pass

class ELSE:
    pass

class TYPE:
    def __init__(self, name: str):
        self.name = name

class SQL:
    def __init__(self, sql: str):
        self.sql: str = sql

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
