from aiogram.utils.keyboard import InlineKeyboardBuilder

def reply_keyboard(mail_id: int):

    builder = InlineKeyboardBuilder()

    builder.button(
        text="✉ Ответить",
        callback_data=f"reply:{mail_id}"
    )

    return builder.as_markup()