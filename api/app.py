import secrets
from datetime import datetime, timezone
from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles

from config import settings
from constants import SECTORS, SPIN_INTERVAL
from logging_config import logger
from schemas import SpinRequest, SpinResponse
from services.store_api import create_promo_code
from services.telegram import check_user_subscribed, send_promo_code, validate_init_data
from storage import get_user_data, set_user_data
from utils import format_timedelta, generate_promo_code

bot_token = settings.bot_token.get_secret_value()

app = FastAPI()

STATIC_DIR = Path("static")
STATIC_DIR.mkdir(exist_ok=True)

app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")


@app.get("/", response_class=HTMLResponse)
async def index():
    index_path = STATIC_DIR / "index.html"
    if not index_path.exists():
        raise HTTPException(status_code=404, detail="index.html not found")
    return index_path.read_text(encoding="utf-8")


@app.get("/sectors")
async def get_sectors():
    return SECTORS


@app.post("/spin", response_model=SpinResponse)
async def spin(req: SpinRequest):
    init_data = validate_init_data(req.init_data)

    user_id = req.user_id
    user_data = get_user_data(user_id)
    now = datetime.now(timezone.utc)

    await check_user_subscribed(user_id)
    last = user_data.get("last_spin")

    if last:
        last_time = datetime.fromisoformat(last)
        next_spin = last_time + SPIN_INTERVAL
        if now < next_spin:
            remaining = next_spin - now
            return {
                "can_spin": False,
                "sector": user_data.get("sector"),
                "promo_code": user_data.get("promo_code"),
                "retry_after": format_timedelta(remaining),
            }

    label = secrets.choice(SECTORS)
    discount = int(label.rstrip("%"))
    promo_code = generate_promo_code()
    username = init_data.user.username or "unknown"

    logger.info(
        f"@{username} (ID {user_id}) hit the wheel — "
        f"sector: {label}, promo code: {promo_code}"
    )

    success = await create_promo_code(username, promo_code, discount)
    if not success:
        raise HTTPException(
            status_code=502, detail="Failed to register promo code in store"
        )

    new_user_data = {
        "last_spin": now.isoformat(),
        "username": username,
        "sector": label,
        "promo_code": promo_code,
    }
    set_user_data(user_id, new_user_data)

    await send_promo_code(int(user_id), label, promo_code)

    return {
        "can_spin": True,
        "sector": label,
        "promo_code": promo_code,
    }
