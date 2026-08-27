class Vault:
    def a(self, key, value):
        self.cells[key] = value

    def b(self, key):
        return self.cells[key]
