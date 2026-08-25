from typing import Any
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder


def get_categories_keyboard(categories: list[dict[str, Any]]) -> InlineKeyboardMarkup:
    """Kategoriyalar ro'yxati inline tugmalari."""
    builder = InlineKeyboardBuilder()
    for cat in categories:
        icon = cat.get("icon") or "🪵"
        name = cat.get("name", "")
        builder.button(
            text=f"{icon} {name}",
            callback_data=f"cat:{cat['id']}"
        )
    builder.adjust(2)
    builder.row(InlineKeyboardButton(text="🔍 Qidiruv", callback_data="search_product"))
    return builder.as_markup()


def get_products_keyboard(products: list[dict[str, Any]], category_id: int) -> InlineKeyboardMarkup:
    """Kategoriya ichidagi mahsulotlar ro'yxati inline tugmalari."""
    builder = InlineKeyboardBuilder()
    for prod in products:
        price = f"{int(float(prod['price'])):,} so'm".replace(",", " ")
        unit = prod.get("unit", {}).get("short_name", "")
        builder.button(
            text=f"{prod['name']} — {price}/{unit}",
            callback_data=f"prod:{prod['id']}"
        )
    builder.adjust(1)
    builder.row(InlineKeyboardButton(text="🔙 Kategoriyalarga qaytish", callback_data="back_to_categories"))
    return builder.as_markup()


def get_product_detail_keyboard(product_id: int, category_id: int, quantity: int = 1) -> InlineKeyboardMarkup:
    """Mahsulot kartasida to'liq interaktiv Numpad klaviaturasi."""
    builder = InlineKeyboardBuilder()
    
    # 1-3 qatori
    builder.row(
        InlineKeyboardButton(text="1", callback_data=f"np:{product_id}:{category_id}:{quantity}:1"),
        InlineKeyboardButton(text="2", callback_data=f"np:{product_id}:{category_id}:{quantity}:2"),
        InlineKeyboardButton(text="3", callback_data=f"np:{product_id}:{category_id}:{quantity}:3"),
    )
    # 4-6 qatori
    builder.row(
        InlineKeyboardButton(text="4", callback_data=f"np:{product_id}:{category_id}:{quantity}:4"),
        InlineKeyboardButton(text="5", callback_data=f"np:{product_id}:{category_id}:{quantity}:5"),
        InlineKeyboardButton(text="6", callback_data=f"np:{product_id}:{category_id}:{quantity}:6"),
    )
    # 7-9 qatori
    builder.row(
        InlineKeyboardButton(text="7", callback_data=f"np:{product_id}:{category_id}:{quantity}:7"),
        InlineKeyboardButton(text="8", callback_data=f"np:{product_id}:{category_id}:{quantity}:8"),
        InlineKeyboardButton(text="9", callback_data=f"np:{product_id}:{category_id}:{quantity}:9"),
    )
    # C, 0, ⌫ qatori
    builder.row(
        InlineKeyboardButton(text="❌ C", callback_data=f"np:{product_id}:{category_id}:{quantity}:c"),
        InlineKeyboardButton(text="0", callback_data=f"np:{product_id}:{category_id}:{quantity}:0"),
        InlineKeyboardButton(text="⌫", callback_data=f"np:{product_id}:{category_id}:{quantity}:del"),
    )

    # Savatga qo'shish tugmasi
    if quantity > 0:
        btn_text = f"🛒 Savatga qo'shish ({quantity:,} ta)".replace(",", " ")
    else:
        btn_text = "🛒 Miqdorni kiriting"

    builder.row(
        InlineKeyboardButton(
            text=btn_text,
            callback_data=f"add_cart:{product_id}:{quantity}"
        )
    )
    
    # Orqaga va Savatcha
    builder.row(
        InlineKeyboardButton(text="🔙 Mahsulotlar", callback_data=f"cat:{category_id}"),
        InlineKeyboardButton(text="🛒 Savatcha", callback_data="view_cart")
    )
    return builder.as_markup()




def get_cart_keyboard(cart_items: list[dict[str, Any]]) -> InlineKeyboardMarkup:
    """Savatchadagi mahsulotlarni boshqarish va buyurtmaga o'tish tugmalari."""
    builder = InlineKeyboardBuilder()

    for item in cart_items:
        prod = item["product"]
        prod_id = prod["id"]
        qty = item["quantity"]
        builder.row(
            InlineKeyboardButton(text=f"❌ {prod['name'][:18]}", callback_data=f"cart_del:{prod_id}"),
            InlineKeyboardButton(text="➖", callback_data=f"cart_dec:{prod_id}"),
            InlineKeyboardButton(text=f"{qty}", callback_data="noop"),
            InlineKeyboardButton(text="➕", callback_data=f"cart_inc:{prod_id}")
        )

    if cart_items:
        builder.row(
            InlineKeyboardButton(text="🗑 Savatni tozalash", callback_data="cart_clear"),
            InlineKeyboardButton(text="📦 Buyurtma berish 🚀", callback_data="checkout_start")
        )
    
    builder.row(
        InlineKeyboardButton(text="🌲 Katalogga qaytish", callback_data="back_to_categories")
    )
    return builder.as_markup()


def get_addresses_selection_keyboard(addresses: list[dict[str, Any]]) -> InlineKeyboardMarkup:
    """Buyurtma paytida manzilni tanlash inline tugmalari."""
    builder = InlineKeyboardBuilder()

    for addr in addresses:
        title = addr.get("title") or "Manzil"
        addr_text = addr.get("address_text", "")

        if addr_text and not addr_text.startswith("GPS:") and not addr_text.startswith("Xarita lokatsiyasi"):
            display_text = f"📍 {addr_text[:28]}..." if len(addr_text) > 28 else f"📍 {addr_text}"
        elif title and title not in ("Manzil", "Geomanzil"):
            display_text = f"📍 {title[:28]}..." if len(title) > 28 else f"📍 {title}"
        else:
            display_text = "📍 Xaritadagi geolokatsiya"

        builder.button(text=display_text, callback_data=f"sel_addr:{addr['id']}")

    builder.adjust(1)
    builder.row(InlineKeyboardButton(text="➕ Yangi manzil kiritish", callback_data="add_new_addr"))
    builder.row(InlineKeyboardButton(text="🔙 Bekor qilish", callback_data="cancel_order"))
    return builder.as_markup()




def get_payment_methods_keyboard() -> InlineKeyboardMarkup:
    """To'lov usulini tanlash tugmalari."""
    builder = InlineKeyboardBuilder()
    builder.button(text="💵 Naqd pul", callback_data="pay_method:cash")
    builder.button(text="💳 Payme", callback_data="pay_method:payme")
    builder.button(text="🔹 Click", callback_data="pay_method:click")
    builder.adjust(1)
    builder.row(InlineKeyboardButton(text="🔙 Bekor qilish", callback_data="cancel_order"))
    return builder.as_markup()


def get_order_confirm_keyboard() -> InlineKeyboardMarkup:
    """Buyurtmani yakuniy tasdiqlash tugmalari."""
    builder = InlineKeyboardBuilder()
    builder.button(text="✅ Buyurtmani tasdiqlayman", callback_data="confirm_order_yes")
    builder.button(text="❌ Bekor qilish", callback_data="cancel_order")
    builder.adjust(1)
    return builder.as_markup()


def get_orders_list_keyboard(orders: list[dict[str, Any]]) -> InlineKeyboardMarkup:
    """Buyurtmalar tarixi ro'yxati tugmalari."""
    builder = InlineKeyboardBuilder()
    for order in orders[:10]:
        status_disp = order.get("status_display") or order.get("status")
        total = f"{int(float(order['total_price'])):,} so'm".replace(",", " ")
        builder.button(
            text=f"📦 #{order['id']} — {total} ({status_disp})",
            callback_data=f"order_view:{order['id']}"
        )
    builder.adjust(1)
    return builder.as_markup()
