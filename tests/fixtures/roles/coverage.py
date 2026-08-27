class Variants:
    def plain(self, value):
        self.x = value

    def aug(self, value):
        self.x += value

    def via_setattr(self, value):
        setattr(self, "x", value)

    def index(self, value):
        self.state["x"] = value

    def read(self):
        return self.x
