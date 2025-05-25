from pydantic import BaseModel


class GetRateParams(BaseModel):
    symbol: str


class GetRateResponse(BaseModel):
    ask_rate: float
    bid_rate: float
    symbol: str
