from core.schemas.coinex import GetRateResponse

from utils.http_client import HttpClient, retry


class CoinexAPI(HttpClient):
    def __init__(self, base_url: str, headers: dict[str, str]):
        super().__init__(base_url=base_url, headers=headers)

    @retry()
    async def get_rate(self, symbol: str) -> GetRateResponse:
        response = await self.get(url="/rate", params={"symbol": symbol})
        return GetRateResponse.model_validate(response)
