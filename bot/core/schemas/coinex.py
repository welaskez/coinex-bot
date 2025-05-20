from pydantic import BaseModel


class GetRateResponseIn(BaseModel):
    symbol: str


class GetRateResponseOut(BaseModel):
    ask_rate: float
    bid_rate: float
    symbol: str
