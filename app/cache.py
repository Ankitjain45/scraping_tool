import shelve

class Cache:
    def __init__(self, filename="cache"):
        self.db = shelve.open(filename)

    def get(self, key):
        return self.db.get(key, None)

    def set(self, key, value):
        self.db[key] = value

    def close(self):
        self.db.close()

    def __del__(self):
        self.close()

