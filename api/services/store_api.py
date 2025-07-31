from datetime import date, datetime, timedelta
from zoneinfo import ZoneInfo

import httpx

from config import settings
from logging_config import logger
from utils import generate_promo_code

MAX_RETRIES = 3


def get_date_range() -> str:
    today = date.today()
    start = today - timedelta(days=1)
    end = today + timedelta(days=7)
    return f"{start.strftime('%d.%m.%Y')} - {end.strftime('%d.%m.%Y')}"


async def register_spin_in_store(user_id: int, user_data: dict):
    username = user_data["username"]
    prize = user_data["prize"]
    spin_time = (
        datetime.fromisoformat(user_data["last_spin"])
        .astimezone(ZoneInfo("Europe/Chisinau"))
        .strftime("%d.%m.%Y %H:%M")
    )

    headers = {
        "Content-Type": "application/json",
        "api-key": settings.store_api_key.get_secret_value(),
    }

    for attempt in range(1, MAX_RETRIES + 1):
        promo_code = user_data["promo_code"]

        payload = {
            "title": (
                f"Wheel of Fortune (telegram bot) | "
                f"@{username} | ID {user_id} | "
                f"{spin_time} | prize: {prize}"
            ),
            "items_type": "all",
            "pcode_type": "once",
            "pcode_date": get_date_range(),
            "visible": 1,
            "pcode_hashes": [
                {
                    "hash": promo_code,
                    "discount": int(prize.rstrip("%")),
                    "quantity": 1,
                }
            ],
        }

        async with httpx.AsyncClient() as client:
            try:
                response = await client.post(
                    settings.store_api_url, json=payload, headers=headers
                )

                if response.headers.get("content-type", "").startswith(
                    "application/json"
                ):
                    data = response.json()
                else:
                    logger.warning(
                        f"Non-JSON response from store API:\n{response.text}"
                    )
                    return False

            except Exception:
                logger.exception("Failed to send promo code to store API:")
                return False

        if data.get("status_code") == 201:
            logger.info(
                "Store confirmed promo registration: "
                f"@{username} | ID {user_id} | {spin_time} | prize: {prize}"
            )
            return True

        elif data.get("status_code") == 409:
            logger.warning(
                f"Promo code already exists: {promo_code}. "
                f"Retrying ({attempt}/{MAX_RETRIES})..."
            )

            user_data["promo_code"] = generate_promo_code()
            continue

        logger.warning(f"Store API returned error: {data}")
        break

    return False
