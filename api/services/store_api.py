from datetime import date, datetime, timedelta
from zoneinfo import ZoneInfo

import httpx

from config import settings
from logging_config import logger


def get_date_range() -> str:
    today = date.today()
    start = today - timedelta(days=1)
    end = today + timedelta(days=7)
    return f"{start.strftime('%d.%m.%Y')} - {end.strftime('%d.%m.%Y')}"


async def register_spin_in_store(user_id: int, user_data: dict) -> bool:
    username = user_data.get("username", "unknown")
    promo_code = user_data["promo_code"]
    prize = user_data["prize"]
    spin_time = (
        datetime.fromisoformat(user_data["last_spin"])
        .astimezone(ZoneInfo("Europe/Chisinau"))
        .strftime("%d.%m.%Y %H:%M")
    )

    payload = {
        "title": (
            f"Wheel of Fortune (telegram bot) | "
            f"@{username} | ID {user_id} | "
            f"{spin_time} | prize: {prize}"
        ),
        "items_type": "all",
        "pcode_type": "once",
        "pcode_date": get_date_range(),
        "items": "",
        "categories": "",
        "visible": 1,
        "pcode_hashes": [
            {
                "hash": promo_code,
                "discount": int(prize.rstrip("%")),
                "quantity": 1,
                "items": "",
                "categories": "",
            }
        ],
    }

    headers = {
        "Content-Type": "application/json",
        "api-key": settings.store_api_key.get_secret_value(),
    }

    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(
                settings.store_api_url, json=payload, headers=headers
            )

            if response.headers.get("content-type", "").startswith("application/json"):
                data = response.json()
            else:
                logger.warning(f"Non-JSON response from store API:\n{response.text}")
                return False

        except Exception:
            logger.exception("Failed to send promo code to store API:")
            return False

    if response.status_code == 201:
        logger.info(data)
        logger.info(f"Promo code created successfully: {promo_code}")
        return True
    else:
        logger.warning(f"Store API returned error: {data}")
        return False
