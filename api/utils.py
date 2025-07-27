import secrets
import string
from datetime import timedelta


def format_timedelta(delta: timedelta) -> str:
    total_seconds = int(delta.total_seconds())
    days, rem = divmod(total_seconds, 86400)
    hours, rem = divmod(rem, 3600)
    minutes, seconds = divmod(rem, 60)

    parts = []
    if days:
        parts.append(f"{days}д")
    if hours:
        parts.append(f"{hours}ч")
    if minutes:
        parts.append(f"{minutes}м")

    if not days and (seconds or not parts):
        parts.append(f"{seconds}с")

    return " ".join(parts)


def generate_promo_code(length=8):
    chars = string.ascii_letters + string.digits
    return "".join(secrets.choice(chars) for _ in range(length))
