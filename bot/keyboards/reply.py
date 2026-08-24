from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def get_main_menu_keyboard() -> ReplyKeyboardMarkup:
    """Asosiy menyu tugmalari."""
    keyboard = [
        [KeyboardButton(text="🌲 Katalog"), KeyboardButton(text="🛒 Savatcha")],
        [KeyboardButton(text="📦 Buyurtmalarim"), KeyboardButton(text="📍 Manzillarim")],
        [KeyboardButton(text="🔍 Qidiruv"), KeyboardButton(text="📞 Bog'lanish")],
    ]
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)


def get_contact_keyboard() -> ReplyKeyboardMarkup:
    """Telefon raqamni yuborish tugmasi."""
    keyboard = [
        [KeyboardButton(text="📱 Telefon raqamni yuborish", request_contact=True)]
    ]
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True, one_time_keyboard=True)


def get_location_keyboard() -> ReplyKeyboardMarkup:
    """Geolokatsiyani yuborish tugmasi."""
    keyboard = [
        [KeyboardButton(text="📍 Joriy manzilni (GPS) yuborish", request_location=True)],
        [KeyboardButton(text="🔙 Bekor qilish")]
    ]
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)


def get_cancel_keyboard() -> ReplyKeyboardMarkup:
    """Bekor qilish tugmasi."""
    keyboard = [
        [KeyboardButton(text="🔙 Bekor qilish")]
    ]
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)


def get_skip_or_cancel_keyboard() -> ReplyKeyboardMarkup:
    """O'tkazib yuborish yoki bekor qilish tugmasi."""
    keyboard = [
        [KeyboardButton(text="⏩ O'tkazib yuborish")],
        [KeyboardButton(text="🔙 Bekor qilish")]
    ]
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)


def get_name_input_keyboard(current_name: str = "") -> ReplyKeyboardMarkup:
    """Ism kiritish uchun klaviatura."""
    keyboard = []
    if current_name:
        keyboard.append([KeyboardButton(text=f"👤 {current_name}")])
    keyboard.append([KeyboardButton(text="🔙 Bekor qilish")])
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)

