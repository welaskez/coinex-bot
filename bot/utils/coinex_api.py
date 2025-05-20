from core.schemas.coinex import GetRateResponseIn, GetRateResponseOut

from utils.http_client import HttpClient, retry


class CoinexAPI(HttpClient):
    def __init__(self, base_url: str, headers: dict[str, str]):
        super().__init__(base_url=base_url, headers=headers)

    @retry()
    async def get_rate(self, symbol: str) -> GetRateResponseOut:
        params = GetRateResponseIn(symbol=symbol).model_dump()
        response = await self.get(url="/rate", params=params)
        return GetRateResponseOut.model_validate(response)
