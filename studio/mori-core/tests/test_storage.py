import json
import shutil
import sys
import tempfile
import unittest
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.core.storage import Storage


class StorageTests(unittest.TestCase):
    def test_storage_creates_expected_json_files(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            storage = Storage(base_dir=tmpdir)
            storage.ensure_files()

            for filename in ["agents.json", "tasks.json", "workflow.json"]:
                path = Path(tmpdir) / filename
                self.assertTrue(path.exists())
                self.assertEqual(json.loads(path.read_text(encoding="utf-8")), {})


if __name__ == "__main__":
    unittest.main()
