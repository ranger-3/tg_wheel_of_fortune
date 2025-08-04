import httpx
from fastapi import HTTPException
from init_data_py import InitData
from init_data_py.errors.errors import UnexpectedFormatError

from config import settings
from logging_config import logger

bot_token = settings.bot_token.get_secret_value()


async def send_promo_code(user_id: int, prize: str | None, promo_code: str | None):
    if prize and promo_code:
        text = (
            f"🎉 Вы выиграли скидку *{prize}*!\n\n"
            f"🎁 Ваш промокод: `{promo_code}`\n\n"
            f"Скопируйте и используйте его в магазине при оформлении заказа\n\n"
            "Колесо можно снова крутить через неделю"
        )
    else:
        text = (
            "Увы, сегодня без промокода\n\n"
            "Но вы сможете снова крутить колесо через неделю"
        )

    async with httpx.AsyncClient() as client:
        await client.post(
            f"https://api.telegram.org/bot{bot_token}/sendMessage",
            json={
                "chat_id": user_id,
                "text": text,
                "parse_mode": "Markdown",
            },
        )


def validate_init_data(raw_init_data: str) -> InitData:
    try:
        init_data = InitData.parse(raw_init_data)
        if not init_data.validate(settings.bot_token.get_secret_value()):
            logger.exception("Invalid Telegram init data")
            raise HTTPException(status_code=400, detail="Invalid Telegram init data")
        return init_data
    except UnexpectedFormatError as e:
        logger.exception("Invalid Telegram init data")
        raise HTTPException(status_code=400, detail="Invalid Telegram init data") from e
    except Exception as e:
        logger.exception("Internal server error")
        raise HTTPException(status_code=500, detail="Internal server error") from e


async def check_user_subscribed(user_id: int) -> None:
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"https://api.telegram.org/bot{bot_token}/getChatMember",
            params={"chat_id": settings.channel_username, "user_id": user_id},
        )
        data = response.json()

        if response.status_code != 200 or not data.get("ok"):
            logger.warning(
                "Failed to verify subscription in WebApp: "
                f"status={response.status_code}, response={data}"
            )
            raise HTTPException(
                status_code=502,
                detail="Failed to verify subscription. Please try again later.",
            )

    user_status = data["result"]["status"]
    if user_status not in ("member", "administrator", "creator"):
        username = data["result"].get("user", {}).get("username", "unknown")
        logger.info(
            f"@{username} (ID {user_id}) is not subscribed — status: '{user_status}'"
        )
        raise HTTPException(
            status_code=403, detail="User is not subscribed to the channel."
        )
