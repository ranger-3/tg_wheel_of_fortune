import json
from pathlib import Path
from typing import Any
from filelock import FileLock

DATA_DIR: Path = Path("data")
DATA_FILE: Path = DATA_DIR / "spin_data.json"
LOCK_FILE: Path = DATA_FILE.with_suffix(".lock")

DATA_DIR.mkdir(parents=True, exist_ok=True)


def load_data() -> dict[str, Any]:
    if not DATA_FILE.exists():
        return {}
    return json.loads(DATA_FILE.read_text(encoding="utf-8"))


def save_data(data: dict[str, Any]) -> None:
    DATA_FILE.write_text(
        json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8"
    )


def get_user_data(user_id: int) -> dict[str, Any]:
    with FileLock(str(LOCK_FILE)):
        data = load_data()
        return data.get(str(user_id), {})


def set_user_data(user_id: int, user_data: dict[str, Any]) -> None:
    with FileLock(str(LOCK_FILE)):
        data = load_data()
        data[str(user_id)] = user_data
        save_data(data)
