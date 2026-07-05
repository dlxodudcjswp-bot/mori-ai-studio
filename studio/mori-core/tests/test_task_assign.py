import sys
import tempfile
import unittest
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.core.storage import Storage
from src.core.task_manager import TaskManager


class TaskAssignTests(unittest.TestCase):
    def test_assign_task_updates_assignee_and_persists_to_storage(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            storage = Storage(base_dir=tmpdir)
            manager = TaskManager(storage=storage)

            task = manager.assign_task("TASK-001", "Developer")

            self.assertIsNotNone(task)
            self.assertEqual(task.assignee, "Developer")
            self.assertEqual(storage.load_json("tasks.json")[0]["assignee"], "Developer")

    def test_assign_task_rejects_unknown_assignee(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            storage = Storage(base_dir=tmpdir)
            manager = TaskManager(storage=storage)

            with self.assertRaises(ValueError):
                manager.assign_task("TASK-001", "Unknown")

    def test_assign_task_returns_none_for_unknown_task(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            storage = Storage(base_dir=tmpdir)
            manager = TaskManager(storage=storage)

            self.assertIsNone(manager.assign_task("UNKNOWN", "QA"))


if __name__ == "__main__":
    unittest.main()
