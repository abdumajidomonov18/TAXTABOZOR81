import logging
from typing import Any, Optional
import httpx
from bot.config import settings

logger = logging.getLogger(__name__)


class APIClient:
    """Django REST Framework backend bilan asinxron aloqa qiluvchi HTTP mijoz."""

    def __init__(self, base_url: str = settings.API_BASE_URL, timeout: float = 10.0):
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout

    async def _request(
        self,
        method: str,
        endpoint: str,
        params: Optional[dict[str, Any]] = None,
        data: Optional[dict[str, Any]] = None,
        json: Optional[dict[str, Any]] = None,
    ) -> Optional[Any]:
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            try:
                response = await client.request(
                    method=method,
                    url=url,
                    params=params,
                    data=data,
                    json=json,
                    headers={"Accept": "application/json"}
                )
                if response.status_code in (200, 201):
                    return response.json()
                elif response.status_code == 204:
                    return True
                else:
                    logger.warning(f"API {method} {url} returned {response.status_code}: {response.text}")
                    try:
                        return {"_error": True, "status": response.status_code, "detail": response.json()}
                    except Exception:
                        return {"_error": True, "status": response.status_code, "detail": response.text}
            except httpx.ConnectError:
                logger.error(f"Backendga ulanib bo'lmadi: {url}")
                return {"_error": True, "detail": "Backend serverga ulanib bo'lmadi"}
            except Exception as e:
                logger.error(f"API so'rovda kutilmagan xato ({url}): {e}")
                return {"_error": True, "detail": str(e)}

    async def get(self, endpoint: str, params: Optional[dict[str, Any]] = None) -> Any:
        return await self._request("GET", endpoint, params=params)

    async def post(self, endpoint: str, json: Optional[dict[str, Any]] = None, params: Optional[dict[str, Any]] = None) -> Any:
        return await self._request("POST", endpoint, params=params, json=json)

    async def patch(self, endpoint: str, json: Optional[dict[str, Any]] = None, params: Optional[dict[str, Any]] = None) -> Any:
        return await self._request("PATCH", endpoint, params=params, json=json)

    async def delete(self, endpoint: str, params: Optional[dict[str, Any]] = None) -> Any:

        return await self._request("DELETE", endpoint, params=params)


api_client = APIClient()
