class CapabilityClient:
    def invoke(self, name, arguments):
        if name == "tools/list":
            return []
        if name == "tools/call":
            return {"ok": True}
        return None

    def schema(self):
        return {"type": "object"}
