import sys
import unittest
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.core.task_manager import TaskManager


class TaskManagerTests(unittest.TestCase):
    def test_task_manager_groups_tasks_by_status(self):
        manager = TaskManager()
        grouped = manager.get_status_groups()

        self.assertGreaterEqual(len(grouped["Todo"]), 1)
        self.assertGreaterEqual(len(grouped["In Progress"]), 1)
        self.assertGreaterEqual(len(grouped["Done"]), 1)
        self.assertIn("Task-008 Task Board", manager.format_board())


if __name__ == "__main__":
    unittest.main()
