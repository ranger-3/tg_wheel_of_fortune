from pydantic import BaseModel


class SpinRequest(BaseModel):
    user_id: int
    init_data: str


class SpinResponse(BaseModel):
    can_spin: bool = True
    prize: str
    promo_code: str | None
    retry_after: str | None = None
