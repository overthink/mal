import reader

def pr_str(data):
    "Return the datastructure data as a string."
    if isinstance(data, list):
        return map(pr_str, data)
    if isinstance(data, int):
        return str(data)
    elif isinstance(data, str):
        # TODO: escaping
        return '"' + data + '"'
    elif data == reader.Nil:
        return "nil"
    elif isinstance(data, reader.MalSymbol):
        return data.name
    elif data == True:
        return "true"
    elif data == False:
        return "false"

if __name__ == '__main__':
    print pr_str("asdf")
    print pr_str(123)
    print pr_str(reader.MalSymbol("sym"))
    print pr_str(reader.Nil)
    print pr_str([1, "two", reader.MalSymbol("three")])

