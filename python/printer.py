"""Mal printer"""
import reader

def pr_str(data):
    "Return the datastructure data as a string."
    if isinstance(data, list):
        return '(' + ' '.join([pr_str(x) for x in data]) + ')'
    elif isinstance(data, int):
        return str(data)
    elif isinstance(data, str):
        return '"' + data + '"'
    elif data == reader.NIL:
        return "nil"
    elif isinstance(data, reader.MalSymbol):
        return data.name
    elif isinstance(data, reader.MalKeyword):
        return ":" + data.name
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

