# services/store_api.py

import httpx
from datetime import date, timedelta
from config import settings
from logging_config import logger


def get_date_range() -> str:
    today = date.today()
    start = today - timedelta(days=1)
    end = today + timedelta(days=7)
    return f"{start.strftime('%d.%m.%Y')} - {end.strftime('%d.%m.%Y')}"


async def create_promo_code(username: str, promo_code: str, discount: int) -> bool:
    payload = {
        "title": f"Wheel of Fortune (telegram bot) date: {date.today():%d.%m.%Y} user: {username}",
        "items_type": "all",
        "pcode_type": "once",
        "pcode_date": get_date_range(),
        "items": "",
        "categories": "",
        "visible": 1,
        "pcode_hashes": [
            {
                "hash": promo_code,
                "discount": discount,
                "quantity": 1,
                "items": "",
                "categories": "",
            }
        ],
    }
    logger.info(payload)

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
