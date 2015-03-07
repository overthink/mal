"""Mal printer"""
import reader
import types

def pr_str(data, print_readably = True):
    "Return the data structure data as a string."
    #print "-- pr_str: " + repr(data)
    #print "--   type: " + str(type(data))
    if isinstance(data, reader.MalList):
        return '(' + ' '.join([pr_str(x) for x in data.value]) + ')'
    elif isinstance(data, list):
        return '[' + ' '.join([pr_str(x) for x in data]) + ']'
    elif isinstance(data, dict):
        return '{' + ' '.join([pr_str(k) + ' ' + pr_str(v) for k, v in data.items()]) + '}'
    # check bools before ints since isinstance(True, bool) == True!
    elif isinstance(data, bool):
        return 'true' if data else 'false'
    elif isinstance(data, int):
        return str(data)
    elif isinstance(data, str):
        if print_readably:
            data = data.replace('"', r'\"')
            data = data.replace('\n', r'\n')
        return '"' + data + '"'
    elif data == reader.NIL:
        return "nil"
    elif isinstance(data, reader.MalSymbol):
        return data.name
    elif isinstance(data, reader.MalKeyword):
        return data.name
    elif isinstance(data, types.FunctionType):
        #return '#' + repr(data.func_code)
        return '#<function>'
    elif data == True:
        return "true"
    elif data == False:
        return "false"
    else:
        raise Exception("can't print: " + repr(data))

if __name__ == '__main__':
    print pr_str("asdf")
    print pr_str(123)
    print pr_str(reader.MalSymbol("sym"))
    print pr_str(reader.NIL)
    print pr_str([1, 'two', [33, reader.MalKeyword('kw'), 44], reader.NIL, reader.MalSymbol('my-sym')])

