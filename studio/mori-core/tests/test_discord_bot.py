import sys
import unittest
from pathlib import Path
from unittest.mock import patch

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.bot.discord_bot import build_command_tree


class DiscordBotTests(unittest.TestCase):
    def test_build_command_tree_registers_expected_commands(self):
        with patch("src.bot.discord_bot.discord.app_commands.CommandTree") as tree_cls:
            tree = build_command_tree()

        self.assertIsNotNone(tree)
        self.assertEqual(tree_cls.call_count, 1)


if __name__ == "__main__":
    unittest.main()
