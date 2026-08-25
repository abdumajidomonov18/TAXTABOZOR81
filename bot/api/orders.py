from typing import Any, Optional
from bot.api.client import api_client


class OrderAPI:
    """Buyurtmalar bilan ishlash uchun API integratsiyasi."""

    @staticmethod
    async def create_order(
        telegram_id: int,
        address_id: int,
        payment_method: str = "cash",
        comment: str = "",
    ) -> dict[str, Any]:
        """Savatdagi mahsulotlardan buyurtma yaratish."""
        payload = {
            "telegram_id": telegram_id,
            "address_id": address_id,
            "payment_method": payment_method,
            "comment": comment,
        }
        return await api_client.post("orders/create/", json=payload)

    @staticmethod
    async def get_orders(telegram_id: int) -> list[dict[str, Any]] | dict[str, Any]:
        """Foydalanuvchining buyurtmalar tarixini olish."""
        return await api_client.get("orders/", params={"telegram_id": telegram_id})

    @staticmethod
    async def get_order_detail(order_id: int) -> dict[str, Any]:
        """Bitta buyurtmaning batafsil ma'lumotlarini olish."""
        return await api_client.get(f"orders/{order_id}/")

    @staticmethod
    async def update_order_status(order_id: int, status_val: str) -> dict[str, Any]:
        """Buyurtma holatini yangilash (admin/xodimlar tomonidan)."""
        return await api_client.patch(f"orders/{order_id}/status/", json={"status": status_val})


order_api = OrderAPI()

