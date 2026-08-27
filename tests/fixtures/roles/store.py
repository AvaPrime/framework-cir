class Store:
    def q(self, item):
        self.state = item

    def z(self):
        return self.state
