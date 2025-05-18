from pydantic import BaseModel


class GetRateResponse(BaseModel):
    ask_rate: float
    bid_rate: float
    symbol: str
