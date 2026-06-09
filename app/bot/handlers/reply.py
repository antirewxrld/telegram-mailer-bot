from aiogram import Router
from aiogram.types import CallbackQuery
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from app.bot.states.reply_state import ReplyState

router = Router()

@router.callback_query(lambda c: c.data.startswith("reply:"))
async def reply_callback(
    callback: CallbackQuery,
    state: FSMContext
):

    mail_id = callback.data.split(":")[1]

    await state.update_data(
        mail_id=mail_id
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

    text = message.text

    data = await state.get_data()

    print(data)

    await message.answer(
        "Ответ отправлен"
    )

    await state.clear()