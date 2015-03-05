class Env:
    "Environment for holding mappings from symbols to MAL values."
    def __init__(self, outer):
        self.outer = outer
        self.data = {}

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
            raise Exception("no value for key " + k)
        return result

