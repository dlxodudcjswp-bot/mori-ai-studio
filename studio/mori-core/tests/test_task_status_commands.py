import sys
import tempfile
import unittest
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.core.storage import Storage
from src.core.task_manager import TaskManager


class TaskStatusCommandTests(unittest.TestCase):
    def test_task_manager_updates_status_and_persists_to_storage(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            storage = Storage(base_dir=tmpdir)
            manager = TaskManager(storage=storage)

            task = manager.update_task_status("TASK-001", "In Progress")
            self.assertIsNotNone(task)
            self.assertEqual(task.status, "In Progress")

            payload = storage.load_json("tasks.json")
            self.assertEqual(payload[0]["status"], "In Progress")

    def test_task_manager_returns_none_for_unknown_task_id(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            storage = Storage(base_dir=tmpdir)
            manager = TaskManager(storage=storage)

            self.assertIsNone(manager.update_task_status("UNKNOWN", "Done"))


if __name__ == "__main__":
    unittest.main()
