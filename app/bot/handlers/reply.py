from aiogram import Router
from aiogram.types import CallbackQuery
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from app.bot.states.reply_state import ReplyState
from app.mail.smtp_client import send_reply

router = Router()

@router.callback_query(lambda c: c.data.startswith("reply|"))
async def reply_callback(
    callback: CallbackQuery,
    state: FSMContext
):

    _, sender, subject = callback.data.split("|")

    await state.update_data(
        sender=sender,
        subject=subject
    )

    await state.set_state(
        ReplyState.waiting_text
    )

    await callback.message.answer(
        "Введите ответ:"
    )

@router.message(ReplyState.waiting_text)
async def send_reply_handler(
    message: Message,
    state: FSMContext
):

    data = await state.get_data()

    sender = data["sender"]
    subject = data["subject"]

    try:

        await send_reply(
            to_email=sender,
            subject=subject,
            text=message.text
        )

        await message.answer(
            "✅ Ответ отправлен"
        )

    except Exception as e:

        await message.answer(
            f"❌ Ошибка:\n{e}"
        )

    await state.clear()