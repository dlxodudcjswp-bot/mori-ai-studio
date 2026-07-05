import sys
import unittest
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.core.workflow_engine import WorkflowEngine


class WorkflowEngineTests(unittest.TestCase):
    def test_workflow_engine_has_expected_stages(self):
        engine = WorkflowEngine()
        lines = engine.get_status_lines()

        self.assertEqual(lines[0], "PM Review: Done")
        self.assertIn("Design: Pending", lines)
        self.assertIn("Development: Pending", lines)
        self.assertIn("QA: Pending", lines)
        self.assertIn("PM Approval: Pending", lines)


if __name__ == "__main__":
    unittest.main()
