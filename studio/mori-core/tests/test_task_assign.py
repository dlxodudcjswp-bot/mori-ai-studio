import sys
import tempfile
import unittest
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.core.agent_manager import AgentManager
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

    def test_task_manager_refreshes_from_storage_after_external_change(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            storage = Storage(base_dir=tmpdir)
            manager_a = TaskManager(storage=storage)
            manager_b = TaskManager(storage=storage)

            manager_a.create_task("New Task", "PM", "High")
            manager_b.refresh()

            self.assertIsNotNone(manager_b.get_task("TASK-004"))

    def test_assign_task_syncs_agent_state_and_persists_it(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            storage = Storage(base_dir=tmpdir)
            agent_manager = AgentManager(storage=storage)
            manager = TaskManager(storage=storage, agent_manager=agent_manager)

            manager.assign_task("TASK-001", "Developer")

            developer = agent_manager.get_agent("developer")
            self.assertIsNotNone(developer)
            self.assertEqual(developer.status, "Working")
            self.assertEqual(developer.current_task, "TASK-001")
            self.assertEqual(storage.load_json("agents.json")["developer"]["current_task"], "TASK-001")

    def test_reassign_task_clears_previous_agent_current_task(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            storage = Storage(base_dir=tmpdir)
            agent_manager = AgentManager(storage=storage)
            manager = TaskManager(storage=storage, agent_manager=agent_manager)

            manager.assign_task("TASK-001", "Developer")
            manager.assign_task("TASK-001", "QA")

            developer = agent_manager.get_agent("developer")
            qa = agent_manager.get_agent("qa")
            self.assertIsNotNone(developer)
            self.assertIsNotNone(qa)
            self.assertIsNone(developer.current_task)
            self.assertEqual(qa.current_task, "TASK-001")
            self.assertEqual(qa.status, "Working")


if __name__ == "__main__":
    unittest.main()
