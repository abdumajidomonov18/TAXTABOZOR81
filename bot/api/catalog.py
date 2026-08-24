from typing import Any, Optional
from bot.api.client import api_client


class CatalogAPI:
    """Kategoriyalar va mahsulotlar bilan ishlovchi API integratsiyasi."""

    @staticmethod
    async def get_categories() -> list[dict[str, Any]] | dict[str, Any]:
        """Barcha mahsulot kategoriyalarini olish."""
        return await api_client.get("products/categories/")

    @staticmethod
    async def get_products(
        category_id: Optional[int] = None,
        search: Optional[str] = None,
        min_price: Optional[float] = None,
        max_price: Optional[float] = None,
    ) -> list[dict[str, Any]] | dict[str, Any]:
        """Filtrlar bo'yicha faol mahsulotlarni olish."""
        params: dict[str, Any] = {}
        if category_id:
            params["category"] = category_id
        if search:
            params["search"] = search
        if min_price is not None:
            params["min_price"] = min_price
        if max_price is not None:
            params["max_price"] = max_price

        return await api_client.get("products/", params=params)

    @staticmethod
    async def get_product(product_id: int) -> dict[str, Any]:
        """Bitta mahsulot tafsilotlarini olish."""
        return await api_client.get(f"products/{product_id}/")


catalog_api = CatalogAPI()
