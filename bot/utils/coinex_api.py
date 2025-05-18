from core.schemas.coinex import UsdtRubPriceResponse

from utils.http_client import HttpClient, retry


class CoinexAPI(HttpClient):
    def __init__(self, base_url: str, headers: dict[str, str]):
        super().__init__(base_url=base_url, headers=headers)

    @retry()
    async def get_usdt_rub_price(self) -> UsdtRubPriceResponse:
        response = await self.get(url="/rate", params={"symbol": "usdtrub"})
        return UsdtRubPriceResponse.model_validate(response)
