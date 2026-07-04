try:
    from dotenv import load_dotenv
except ImportError:  # pragma: no cover - graceful fallback for bootstrap
    def load_dotenv() -> bool:
        return False


def main() -> None:
    load_dotenv()
    print("Mori Core v0.1 Booting...")


if __name__ == "__main__":
    main()
