import json
from pathlib import Path

class CommitCheckpoint:
    def __init__(self, path):
        self.path = Path(path)

    def load(self):
        if not self.path.exists():
            return None
        return json.loads(self.path.read_text())["commit"]

    def save_after_publish(self, commit):
        self.path.parent.mkdir(parents=True, exist_ok=True)
        tmp = self.path.with_suffix(".tmp")
        tmp.write_text(json.dumps({"commit": commit}))
        tmp.replace(self.path)
