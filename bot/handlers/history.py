from aiogram import Router, F, types
from aiogram.fsm.context import FSMContext

from bot.api.orders import order_api
from bot.keyboards.inline import get_orders_list_keyboard
from bot.keyboards.reply import get_main_menu_keyboard

router = Router()


@router.message(F.text == "📦 Buyurtmalarim")
async def show_orders_history(message: types.Message, state: FSMContext):
    """Foydalanuvchining buyurtmalar tarixini ko'rsatish."""
    await state.clear()
    telegram_id = message.from_user.id
    orders = await order_api.get_orders(telegram_id)

    if isinstance(orders, dict) and orders.get("_error"):
        await message.answer("⚠️ Buyurtmalar tarixini yuklashda xatolik yuz berdi.")
        return

    if not orders:
        await message.answer(
            "📦 <b>Sizda hali buyurtmalar mavjud emas.</b>\n\nKatalog orqali buyurtma berishingiz mumkin.",
            parse_mode="HTML"
        )
        return

    text = "📦 <b>Sizning oxirgi buyurtmalaringiz:</b>\n\nBatafsil ma'lumot olish uchun buyurtmani tanlang:"
    reply_markup = get_orders_list_keyboard(orders)
    await message.answer(text, reply_markup=reply_markup, parse_mode="HTML")


@router.callback_query(F.data.startswith("order_view:"))
async def show_order_detail(callback: types.CallbackQuery):
    """Tanlangan buyurtma tafsilotlarini ko'rsatish."""
    order_id = int(callback.data.split(":")[1])
    order = await order_api.get_order_detail(order_id)

    if isinstance(order, dict) and order.get("_error"):
        await callback.answer("⚠️ Buyurtma tafsilotlarini yuklab bo'lmadi.", show_alert=True)
        return

    total = f"{int(float(order.get('total_price', 0))):,} so'm".replace(",", " ")
    status_disp = order.get("status_display") or order.get("status")
    created_at = order.get("created_at", "")[:10]
    payment = order.get("payment_method", "cash").upper()
    address = order.get("address_text", "")
    items = order.get("items", [])

    lines = [
        f"📦 <b>Buyurtma #{order_id}</b>",
        f"📅 <b>Sana:</b> {created_at}",
        f"📊 <b>Holati:</b> {status_disp}",
        f"💳 <b>To'lov turi:</b> {payment}",
        f"📍 <b>Manzil:</b> {address}\n",
        "📋 <b>Tarkibi:</b>"
    ]

    for idx, item in enumerate(items, 1):
        price = f"{int(float(item.get('price', 0))):,} so'm".replace(",", " ")
        subtotal = f"{int(float(item.get('subtotal', 0))):,} so'm".replace(",", " ")
        lines.append(
            f"{idx}. {item.get('product_name')} — {item.get('quantity')} dona × {price} = {subtotal}"
        )

    lines.append(f"\n💰 <b>Jami summa:</b> <b>{total}</b>")

    await callback.message.answer("\n".join(lines), parse_mode="HTML")
    await callback.answer()
