from typing import Any, Optional
from bot.api.client import api_client


class UserAPI:
    """Foydalanuvchilar va manzillar bilan ishlovchi API integratsiyasi."""

    @staticmethod
    async def register_user(telegram_id: int, phone_number: str, full_name: str = "") -> dict[str, Any]:
        """Foydalanuvchini ro'yxatdan o'tkazish yoki mavjudini olish."""
        payload = {
            "telegram_id": telegram_id,
            "phone_number": phone_number,
            "full_name": full_name,
        }
        return await api_client.post("users/register/", json=payload)

    @staticmethod
    async def get_user_profile(telegram_id: int) -> dict[str, Any]:
        """Foydalanuvchi profili va manzillarini olish."""
        return await api_client.get("users/me/", params={"telegram_id": telegram_id})

    @staticmethod
    async def update_user_name(telegram_id: int, full_name: str) -> dict[str, Any]:
        """Foydalanuvchi ism va familiyasini yangilash."""
        return await api_client.patch("users/me/", json={"telegram_id": telegram_id, "full_name": full_name})


    @staticmethod
    async def get_addresses(telegram_id: int) -> list[dict[str, Any]] | dict[str, Any]:
        """Foydalanuvchining barcha yetkazib berish manzillarini olish."""
        return await api_client.get("users/addresses/", params={"telegram_id": telegram_id})

    @staticmethod
    async def add_address(
        telegram_id: int,
        title: str,
        address_text: str,
        latitude: float = 0.0,
        longitude: float = 0.0,
        is_default: bool = False,
    ) -> dict[str, Any]:
        """Yangi yetkazib berish manzilini qo'shish."""
        payload = {
            "title": title,
            "address_text": address_text,
            "latitude": round(latitude, 6) if latitude else 0,
            "longitude": round(longitude, 6) if longitude else 0,
            "is_default": is_default,
        }
        return await api_client.post("users/addresses/", json=payload, params={"telegram_id": telegram_id})


    @staticmethod
    async def delete_address(address_id: int) -> dict[str, Any]:
        """Manzilni o'chirish."""
        return await api_client.delete(f"users/addresses/{address_id}/")


user_api = UserAPI()
