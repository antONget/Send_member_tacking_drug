from aiogram.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup, InputMediaPhoto
from aiogram import F, Router, Bot
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.filters import StateFilter

from keyboards.user import keyboard_registration as kb
from utils.error_handling import error_handler

from utils.message_day_tacking_drug import message_day_volume
from database import requests as rq
from database.models import Drug, TakingDrug, User
from config_data.config import Config, load_config
import logging

router = Router()
config: Config = load_config()


class StateRegistration(StatesGroup):
    fullname = State()
    age = State()


@router.callback_query(F.data.startswith('collagen'))
@error_handler
async def process_start_yes(callback: CallbackQuery, state: FSMContext, bot: Bot):
    """
    Начало регистрации
    :param callback:
    :param state:
    :param bot:
    :return:
    """
    logging.info('process_start_yes')
    drug_id = int(callback.data.split('_')[-1])
    await rq.set_drug_intake(drug_id=drug_id,
                             intake=1)
    data_taking_drug = {"tg_id": callback.from_user.id,
                        "drag_id": drug_id,
                        "bonus": 50}
    await rq.add_taking_drug(data=data_taking_drug)
    drug_info: Drug = await rq.get_drug_id(drug_id=drug_id)
    await rq.set_user_balance(tg_id=drug_info.tg_id,
                              balance=50)
    await rq.set_drug_balance(drug_id=drug_info.id,
                              balance=50)
    tacking_drugs: list[TakingDrug] = await rq.get_taking_drug_id(drag_id=drug_info.id)
    day = drug_info.start_day
    if tacking_drugs:
        day += len(tacking_drugs)
    dict_message: dict = await message_day_volume(day=day,
                                                  volume=drug_info.volume_drug)
    user_info: User = await rq.get_user_by_id(tg_id=drug_info.tg_id)
    await callback.message.edit_media(media=InputMediaPhoto(media=dict_message["image_id"],
                                                            caption=f'<b>День: {day}.</b>\n\n'
                                                                    f'{dict_message["pozitive"]}\n\n'
                                                                    f'Ваш баланс: {user_info.balance_user} баллов'),
                                      reply_markup=None)
    if drug_info.volume_drug == (drug_info.start_day + len(tacking_drugs)):
        await rq.set_drug_status(drug_id=drug_id,
                                 status=rq.StatusDrug.completed)
        button = InlineKeyboardButton(text='Оставить отзыв',
                                      callback_data=f'feedback_{drug_info.id}')
        keyboard = InlineKeyboardMarkup(inline_keyboard=[[button]])
        await bot.send_message(chat_id=drug_info.tg_id,
                               text='🤝Благодарю вас за выбор продукции PP Lab для укрепления и поддержки'
                                    ' своего здоровья. Если вы соблюдали все мои рекомендации и'
                                    ' придерживались графика, то уже могли заметить положительное'
                                    ' влияние коллагена на ваше внутреннее и внешнее состояние.\n\n'
                                    '<b>Мне бы хотелось узнать об этих изменениях. Почувствовали ли вы'
                                    ' прилив энергии, улучшилось ли состояние кожи или что-то еще приятно'
                                    ' вас удивило? Расскажите нам об этом.</b>\n\n'
                                    '1. Оставьте ваш отзыв о продукте на маркетплейсе, где была совершена покупка.\n'
                                    '2. Пришлите сюда скриншот отзыва ⤵️\n'
                                    '3. В благодарность за уделенное время и ценную информацию вы получите'
                                    ' дополнительные бонусные баллы🎁.',
                               reply_markup=keyboard)
    await callback.answer()
