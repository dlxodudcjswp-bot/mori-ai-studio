import os
import sys
import unittest
from pathlib import Path
from unittest.mock import AsyncMock, patch

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.bot.discord_bot import build_command_tree, sync_commands


class DiscordBotTests(unittest.TestCase):
    def test_build_command_tree_registers_expected_commands(self):
        with patch("src.bot.discord_bot.discord.app_commands.CommandTree") as tree_cls:
            tree = build_command_tree()

        self.assertIsNotNone(tree)
        self.assertEqual(tree_cls.call_count, 1)

    def test_build_command_tree_registers_agent_commands(self):
        tree = build_command_tree()
        command_names = [command.name for command in tree.get_commands()]

        for expected in ["ping", "status", "help", "pm", "designer", "developer", "qa"]:
            self.assertIn(expected, command_names)


class SyncCommandTests(unittest.IsolatedAsyncioTestCase):
    async def test_sync_commands_uses_guild_scope_when_configured(self):
        tree = AsyncMock()
        tree.sync = AsyncMock(return_value=[object()])

        with patch.dict(os.environ, {"DISCORD_GUILD_ID": "123456789"}, clear=False):
            count = await sync_commands(tree)

        self.assertEqual(count, 1)
        tree.sync.assert_awaited_once()
        self.assertEqual(tree.sync.await_args.kwargs["guild"].id, 123456789)


if __name__ == "__main__":
    unittest.main()
