import sys
import tempfile
import unittest
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.core.storage import Storage
from src.core.task_manager import TaskManager


class TaskCreateTests(unittest.TestCase):
    def test_task_manager_creates_task_with_generated_id_and_persists_it(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            storage = Storage(base_dir=tmpdir)
            manager = TaskManager(storage=storage)

            task = manager.create_task(title="New Task", assignee="PM", priority="High")

            self.assertEqual(task.id, "TASK-004")
            self.assertEqual(task.status, "Todo")
            self.assertEqual(storage.load_json("tasks.json")[-1]["title"], "New Task")


if __name__ == "__main__":
    unittest.main()
