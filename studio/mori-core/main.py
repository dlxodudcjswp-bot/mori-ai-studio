import os
import sys
from pathlib import Path

try:
    from dotenv import load_dotenv
except ImportError:  # pragma: no cover - graceful fallback for bootstrap
    def load_dotenv() -> bool:
        return False

PROJECT_ROOT = Path(__file__).resolve().parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

try:
    from src.bot.discord_bot import start_discord_bot
except ImportError:  # pragma: no cover - graceful fallback for bootstrap
    def start_discord_bot(token: str) -> None:
        raise RuntimeError("discord.py is not installed")


def main() -> None:
    load_dotenv()
    print("Mori Core v0.2 Booting...")
    print("환경변수 확인")

    token = os.getenv("DISCORD_BOT_TOKEN", "").strip()
    if not token:
        print("Discord token not found.")
        print("Running in Local Mode.")
        return

    print("Discord Bot 실행")
    start_discord_bot(token)


if __name__ == "__main__":
    main()
