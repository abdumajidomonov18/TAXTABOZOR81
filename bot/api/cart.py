from typing import Any
from bot.api.client import api_client


class CartAPI:
    """Savatcha amallari uchun API integratsiyasi."""

    @staticmethod
    async def get_cart(telegram_id: int) -> dict[str, Any]:
        """Foydalanuvchining savatini va undagi mahsulotlarni olish."""
        return await api_client.get("cart/", params={"telegram_id": telegram_id})

    @staticmethod
    async def add_to_cart(telegram_id: int, product_id: int, quantity: int = 1) -> dict[str, Any]:
        """Savatga mahsulot qo'shish yoki miqdorini oshirish."""
        payload = {
            "telegram_id": telegram_id,
            "product_id": product_id,
            "quantity": quantity,
        }
        return await api_client.post("cart/add/", json=payload)

    @staticmethod
    async def remove_from_cart(telegram_id: int, product_id: int, quantity: int = 1) -> dict[str, Any]:
        """Savatdan mahsulot miqdorini kamaytirish yoki butunlay o'chirish (quantity=0)."""
        payload = {
            "telegram_id": telegram_id,
            "product_id": product_id,
            "quantity": quantity,
        }
        return await api_client.post("cart/remove/", json=payload)

    @staticmethod
    async def clear_cart(telegram_id: int) -> dict[str, Any]:
        """Savatni to'liq tozalash."""
        payload = {"telegram_id": telegram_id}
        return await api_client.post("cart/clear/", json=payload)


cart_api = CartAPI()
