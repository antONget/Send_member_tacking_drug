import datetime

from aiogram.types import CallbackQuery, Message, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram import F, Router, Bot
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.filters import StateFilter

from utils.error_handling import error_handler
from config_data.config import Config, load_config
from database import requests as rq
from database.models import Drug, User
from utils.send_admins import send_message_admins_text
import logging

router = Router()
config: Config = load_config()


class StateFeedBack(StatesGroup):
    feedback = State()


@router.callback_query(F.data.startswith('feedback_'))
@error_handler
async def process_feedback(callback: CallbackQuery, state: FSMContext, bot: Bot):
    """
    Начало регистрации
    :param callback:
    :param state:
    :param bot:
    :return:
    """
    logging.info('process_feedback')
    drug_id = int(callback.data.split('_')[-1])
    await state.update_data(feedback_drug_id=drug_id)
    info_drug: Drug = await rq.get_drug_id(drug_id=drug_id)
    taste_drug = info_drug.taste_drug
    volume_drug = info_drug.volume_drug
    taste = 'грейпфрута'
    if taste_drug == 'limon':
        taste = 'лимона'
    elif taste_drug == 'orange':
        taste = 'апельсина'
    await callback.message.edit_text(text=f'Пришлите отзыв за прием препарата: Collagen Jelly PP Lab со вкусом {taste}'
                                          f' - {volume_drug} саше',
                                     reply_markup=None)
    await state.set_state(StateFeedBack.feedback)
    await callback.answer()


@router.message(F.text == 'Оставить отзыв')
@error_handler
async def process_feedback(message: Message, state: FSMContext, bot: Bot):
    """
    Отзыв
    :param message:
    :param state:
    :param bot:
    :return:
    """
    logging.info('process_feedback')
    await message.answer(text=f'1. Оставьте ваш отзыв о продукте на маркетплейсе, где была совершена покупка.\n'
                                 f'2. Пришлите сюда скриншот отзыва ⤵️\n'
                                 f'3. В благодарность за уделенное время и ценную информацию вы получите'
                                 f' дополнительные бонусные баллы🎁.')
    await state.set_state(StateFeedBack.feedback)


@router.message(StateFilter(StateFeedBack.feedback))
@error_handler
async def get_feedback(message: Message, state: FSMContext, bot: Bot):
    """
    Получаем отзыв
    :param message:
    :param state:
    :param bot:
    :return:
    """
    logging.info('get_feedback')
    photo = message.photo
    if photo:
        photo = message.photo[-1].file_id
    else:
        await message.answer(text='Мы ждем от вас скриншот отзыва')
        return

    drugs_user: list[Drug] = await rq.get_drug_last_tg_id(tg_id=message.from_user.id)
    if drugs_user:
        feedback_drug_id = drugs_user[-1].id
        info_drug: Drug = await rq.get_drug_id(drug_id=feedback_drug_id)
        info_user: User = await rq.get_user_by_id(tg_id=info_drug.tg_id)
        data_feedback = {
            "tg_id": message.from_user.id,
            "drug_id": feedback_drug_id,
            "feedback": photo
        }
        await rq.add_feed_back(data=data_feedback)
        taste_drug = info_drug.taste_drug
        volume_drug = info_drug.volume_drug
        taste = 'грейпфрута'
        if taste_drug == 'limon':
            taste = 'лимона'
        elif taste_drug == 'orange':
            taste = 'апельсина'
        button_1 = InlineKeyboardButton(text='Подтвердить',
                                      callback_data=f'adminfeedback_confirm_{message.from_user.id}')
        button_2 = InlineKeyboardButton(text='Отклонить',
                                      callback_data=f'adminfeedback_сфтсуд_{message.from_user.id}')
        keyboard = InlineKeyboardMarkup(inline_keyboard=[[button_1], [button_2]])
        await bot.send_photo(photo=photo,
                             chat_id=config.tg_bot.group_id,
                             caption=f'От пользователя'
                                     f' <a href="https://t.me/userid?id={info_drug.tg_id}">{info_user.fullname}</a> '
                                     f'получен отзыв по курс приема препарата.\n\n'
                                     f'<b>Информация о препарате:</b>\n'
                                     f'Название: Collagen Jelly PP Lab со вкусом {taste} - {volume_drug} саше\n'
                                     f'Место приобретения: {info_drug.marketplace}\n'
                                     f'Курс приема с {info_drug.data_start_tacking}\n'
                                     f'<b>Информация о пользователе:</b>\n'
                                     f'Имя: {info_user.fullname}\n'
                                     f'Возраст: {info_user.age}\n'
                                     f'Баланс: {info_user.balance_user} баллов',
                             reply_markup=keyboard)
        await message.answer(text=f'✨Спасибо за обратную связь. Ваш отзыв отправлен на модерацию.')
