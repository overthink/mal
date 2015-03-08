from core import s

class Env:
    "Environment for holding mappings from symbols to MAL values."
    def __init__(self, outer, binds, exprs):
        self.outer = outer
        self.data = {}
        for i in xrange(len(binds)):
            bind = binds[i]
            if bind == s('&'):
                next_bind = binds[i + 1]
                rest_exprs = exprs[i:]
                self.set(next_bind, rest_exprs)
                break
            else:
                self.set(bind, exprs[i])

    def set(self, k, v):
        self.data[k] = v

    def find(self, k):
        result = self.data.get(k)
        if result is None and self.outer is not None:
            return self.outer.find(k)
        else:
            return result

    def get(self, k):
        result = self.find(k)
        if result is None:
            raise Exception("no value for key {0}".format(k))
        return result

