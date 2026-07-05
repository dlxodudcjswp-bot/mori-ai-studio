import sys
import unittest
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.core.agent_manager import AgentManager


class AgentManagerTests(unittest.TestCase):
    def test_agent_manager_exposes_default_idle_agents(self):
        manager = AgentManager()

        self.assertEqual(manager.get_agent("pm").status, "Idle")
        self.assertEqual(manager.get_agent("designer").status, "Idle")
        self.assertEqual(manager.get_agent("developer").status, "Idle")
        self.assertEqual(manager.get_agent("qa").status, "Idle")
        self.assertEqual(manager.get_status_lines(), [
            "PM\nStatus: Idle\nCurrent Task: None",
            "Designer\nStatus: Idle\nCurrent Task: None",
            "Developer\nStatus: Idle\nCurrent Task: None",
            "QA\nStatus: Idle\nCurrent Task: None",
        ])


if __name__ == "__main__":
    unittest.main()
