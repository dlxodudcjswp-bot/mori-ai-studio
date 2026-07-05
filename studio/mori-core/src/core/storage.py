import json
from pathlib import Path
from typing import Any


class Storage:
    def __init__(self, base_dir: str | None = None) -> None:
        self.base_dir = Path(base_dir or Path(__file__).resolve().parents[1] / "data")
        self.base_dir.mkdir(parents=True, exist_ok=True)

    def _path(self, filename: str) -> Path:
        return self.base_dir / filename

    def ensure_files(self) -> None:
        for filename in ["agents.json", "tasks.json", "workflow.json"]:
            path = self._path(filename)
            if not path.exists():
                path.write_text("{}", encoding="utf-8")

    def load_json(self, filename: str) -> Any:
        self.ensure_files()
        path = self._path(filename)
        if not path.exists():
            return {}
        with path.open("r", encoding="utf-8") as handle:
            return json.load(handle)

    def save_json(self, filename: str, payload: Any) -> None:
        self.ensure_files()
        path = self._path(filename)
        with path.open("w", encoding="utf-8") as handle:
            json.dump(payload, handle, indent=2)
            handle.write("\n")
