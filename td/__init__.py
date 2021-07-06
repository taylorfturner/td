from pathlib import Path

from dotenv import load_dotenv

load_dotenv()


def project_root():
    return Path(__file__).parent.parent.resolve()
