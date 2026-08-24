from aiogram import Router
from .start import router as start_router
from .catalog import router as catalog_router
from .cart import router as cart_router
from .order import router as order_router
from .history import router as history_router
from .common import router as common_router


def setup_routers() -> list[Router]:
    """Barcha handler routerlarini birlashtirish."""
    return [
        start_router,
        catalog_router,
        cart_router,
        order_router,
        history_router,
        common_router,
    ]
