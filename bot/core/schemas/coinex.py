from pydantic import BaseModel


class UsdtRubPriceResponse(BaseModel):
    ask_rate: float
    bid_rate: float
    symbol: str
