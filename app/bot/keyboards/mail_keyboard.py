from aiogram.utils.keyboard import InlineKeyboardBuilder

def reply_keyboard(sender, subject):

    builder = InlineKeyboardBuilder()

    data = f"reply|{sender}|{subject}"

    builder.button(
        text="✉ Ответить",
        callback_data=data[:64]
    )

    return builder.as_markup()