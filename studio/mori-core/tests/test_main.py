import io
import os
import sys
import unittest
from contextlib import redirect_stdout
from pathlib import Path
from unittest.mock import patch

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import main


class MainTests(unittest.TestCase):
    def test_main_prints_local_mode_when_token_missing(self):
        with patch.dict(os.environ, {}, clear=True):
            output = io.StringIO()
            with redirect_stdout(output):
                main.main()

        stdout = output.getvalue()
        self.assertIn("Mori Core v0.2 Booting...", stdout)
        self.assertIn("환경변수 확인", stdout)
        self.assertIn("Discord token not found.", stdout)
        self.assertIn("Running in Local Mode.", stdout)

    def test_main_starts_discord_bot_when_token_present(self):
        with patch.dict(os.environ, {"DISCORD_BOT_TOKEN": "test-token"}, clear=True):
            with patch("main.start_discord_bot") as mock_start:
                output = io.StringIO()
                with redirect_stdout(output):
                    main.main()

        mock_start.assert_called_once_with("test-token")
        self.assertIn("Discord Bot 실행", output.getvalue())


if __name__ == "__main__":
    unittest.main()
