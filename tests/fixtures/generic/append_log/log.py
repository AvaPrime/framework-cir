class Transcript:
    def __init__(self):
        self.messages = []

    def record(self, message):
        self.messages.append(message)
