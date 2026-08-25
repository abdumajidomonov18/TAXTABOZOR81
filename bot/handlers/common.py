from aiogram import Router, F, types
from aiogram.fsm.context import FSMContext
from aiogram.utils.keyboard import InlineKeyboardBuilder

from bot.api.users import user_api
from bot.keyboards.reply import get_main_menu_keyboard

router = Router()


@router.message(F.text == "📍 Manzillarim")
async def show_my_addresses(message: types.Message, state: FSMContext):
    """Foydalanuvchining saqlangan manzillarini ko'rsatish."""
    await state.clear()
    telegram_id = message.from_user.id
    addresses = await user_api.get_addresses(telegram_id)

    if isinstance(addresses, dict) and addresses.get("_error"):
        await message.answer("⚠️ Manzillarni yuklashda xatolik yuz berdi.")
        return

    if not addresses:
        await message.answer(
            "📍 <b>Sizda hali saqlangan manzillar yo'q.</b>\n\nBuyurtma berish paytida manzilingizni kiritishingiz mumkin.",
            parse_mode="HTML"
        )
        return

    lines = ["📍 <b>Sizning saqlangan yetkazib berish manzillaringiz:</b>\n"]
    builder = InlineKeyboardBuilder()

    for idx, addr in enumerate(addresses, 1):
        title = addr.get("title") or "Manzil"
        addr_text = addr.get("address_text", "")
        addr_id = addr.get("id")
        
        lines.append(f"{idx}. 🏷 <b>{title}</b>\n   └ <i>{addr_text}</i>")
        builder.button(text=f"🗑 O'chirish: {title}", callback_data=f"del_addr:{addr_id}")

    lines.append("\n<i>Manzilni o'chirish uchun pastdagi tegishli tugmani bosing:</i>")
    builder.adjust(1)
    await message.answer("\n".join(lines), reply_markup=builder.as_markup(), parse_mode="HTML")



@router.callback_query(F.data.startswith("del_addr:"))
async def delete_address_callback(callback: types.CallbackQuery):
    """Manzilni o'chirish."""
    addr_id = int(callback.data.split(":")[1])
    await user_api.delete_address(addr_id)
    await callback.answer("Manzil o'chirildi", show_alert=True)
    await callback.message.delete()


@router.message(F.text == "📞 Bog'lanish")
async def show_contacts(message: types.Message):
    """Do'kon bilan aloqa ma'lumotlari."""
    text = (
        "🏢 <b>TAXTABOZOR81 — Qurilish mollari va taxta bozori</b>\n\n"
        "📞 <b>Telefon:</b> +998 90 123 45 67\n"
        "💬 <b>Telegram:</b> @taxtabozor81_admin\n"
        "⏰ <b>Ish vaqti:</b> 08:00 — 19:00 (Har kuni)\n"
        "📍 <b>Manzil:</b> Toshkent sh., Taxta bozori, 81-do'kon\n\n"
        "Har qanday savollar bo'yicha murojaat qilishingiz mumkin!"
    )
    await message.answer(text, parse_mode="HTML")


@router.callback_query(F.data == "noop")
async def noop_callback(callback: types.CallbackQuery):
    """Bo'sh tugma uchun javob."""
    await callback.answer()


@router.message(F.text == "🔙 Bekor qilish")
async def cancel_any_action(message: types.Message, state: FSMContext):
    """Har qanday jarayonni bekor qilish."""
    await state.clear()
    await message.answer("Bosh menyu:", reply_markup=get_main_menu_keyboard())
