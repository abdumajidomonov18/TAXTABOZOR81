import asyncio
import logging
import sys

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage

from bot.config import settings
from bot.handlers import setup_routers

# Loglashni sozlash
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    stream=sys.stdout,
)
logger = logging.getLogger("TAXTABOZOR_BOT")


async def main():
    """Botni ishga tushirish funktsiyasi."""
    if not settings.BOT_TOKEN:
        logger.error(
            "BOT_TOKEN topilmadi! Iltimos, bot/.env fayliga BOT_TOKEN qiymatini kiriting."
        )
        return

    # Bot va Dispatcher yaratish
    bot = Bot(
        token=settings.BOT_TOKEN,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML),
    )
    dp = Dispatcher(storage=MemoryStorage())

    # Barcha routerlarni ro'yxatdan o'tkazish
    for router in setup_routers():
        dp.include_router(router)

    logger.info("Bot muvaffaqiyatli ishga tushirildi. Polling boshlanmoqda...")
    try:
        # Eski kutilayotgan yangilanishlarni o'chirish va pollingni boshlash
        await bot.delete_webhook(drop_pending_updates=True)
        await dp.start_polling(bot)
    finally:
        await bot.session.close()
        logger.info("Bot to'xtatildi.")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.info("Bot qo'lda to'xtatildi.")
