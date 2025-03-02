import datetime

from aiogram.types import CallbackQuery, Message
from aiogram import F, Router, Bot
from aiogram.fsm.context import FSMContext
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from keyboards.admin import keyboard_edit_card as kb
from utils.error_handling import error_handler
from utils.utils_keyboard import utils_handler_pagination_one_card_photo_or_only_text
from filter.admin_filter import IsSuperAdmin
from config_data.config import Config, load_config
from database.models import User
from database import requests as rq
import logging

router = Router()
config: Config = load_config()


@router.callback_query(F.data.startswith('adminfeedback'))
@error_handler
async def process_adminfeedback(callback: CallbackQuery, state: FSMContext, bot: Bot):
    """
    Подтверждение отзыва
    :param callback:
    :param state:
    :param bot:
    :return:
    """
    logging.info('process_adminfeedback')
    action = callback.data.split('_')[-2]
    user_tg_id = int(callback.data.split('_')[-1])
    if action == 'confirm':
        await callback.message.edit_reply_markup(reply_markup=None)
        await callback.message.answer(text='Отзыв подтвержден')
        await bot.send_message(chat_id=user_tg_id,
                               text=f'✨Спасибо за обратную связь. В знак благодарности за ваш отзыв вы получаете еще'
                                    f' 250 бонусных баллов.')
        await rq.set_user_balance(tg_id=user_tg_id,
                                  balance=250)
    else:
        await callback.message.edit_reply_markup(reply_markup=None)
        await callback.message.answer(text='Отзыв отклонен')
        await bot.send_message(chat_id=user_tg_id,
                               text=f'Ваш отзыв отклонен')