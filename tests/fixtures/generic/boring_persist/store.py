class CompletelyBoringObject:
    def persist(self, run_id, state):
        path = f"/tmp/{run_id}.bin"
        with open(path, "w", encoding="utf-8") as handle:
            handle.write(str(state))

    def restore(self, run_id):
        path = f"/tmp/{run_id}.bin"
        with open(path, encoding="utf-8") as handle:
            return handle.read()
