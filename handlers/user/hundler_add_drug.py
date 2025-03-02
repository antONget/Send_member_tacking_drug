import datetime

from aiogram.types import CallbackQuery, Message, InputMediaPhoto
from aiogram import F, Router, Bot
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.filters import StateFilter

from keyboards.user import keyboard_add_drug as kb
from utils.error_handling import error_handler
from filter.filter import validate_date, validate_time
from config_data.config import Config, load_config
from database import requests as rq
import logging

router = Router()
config: Config = load_config()


class StateDrug(StatesGroup):
    marketplace = State()
    data_start = State()
    time_start = State()


@router.callback_query(F.data.startswith('marketplace_'))
@error_handler
async def process_select_marketplace(callback: CallbackQuery, state: FSMContext, bot: Bot):
    """
    Начало регистрации
    :param callback:
    :param state:
    :param bot:
    :return:
    """
    logging.info('process_select_marketplace')
    marketplace = callback.data.split('_')[-1]
    await state.update_data(marketplace=marketplace)
    if marketplace == 'other':
        await callback.message.edit_text(text="""Напишите название клиники или магазина, где вы приобрели коллаген.""")
        await state.set_state(StateDrug.marketplace)
    else:
        await callback.message.edit_text(text="💖Все почти готово. Осталось выбрать из списка, какой именно коллаген"
                                              " PP Lab вы планируете принимать.\n\n"
                                              "Важно! Проверьте, какое количество саше указано на вашей упаковке.\n"
                                              "Collagen Jelly PP Lab:",
                                         reply_markup=kb.keyboard_select_drug())
    await callback.answer()


@router.message(F.text, StateFilter(StateDrug.marketplace))
@error_handler
async def get_marketplace(message: Message, state: FSMContext, bot: Bot):
    """
    Получаем другое место приобретения препарата
    :param message:
    :param state:
    :param bot:
    :return:
    """
    logging.info('get_full_name')
    name_marketplace = message.text
    await state.update_data(marketplace=name_marketplace)
    await message.answer(text="💖Все почти готово. Осталось выбрать из списка, какой именно коллаген PP Lab вы"
                              " планируете принимать.\n\n"
                              "Важно! Проверьте, какое количество саше указано на вашей упаковке.\n\n"
                              "Collagen Jelly PP Lab:",
                            reply_markup=kb.keyboard_select_drug())


@router.callback_query(F.data.startswith('type_drug_'))
@error_handler
async def get_type_drug_(callback: CallbackQuery, state: FSMContext, bot: Bot):
    """
    Получаем вид препарата
    :param callback: type_drug_grapefruit_30
    :param state:
    :param bot:
    :return:
    """
    logging.info('get_type_drug_')
    volume = callback.data.split('_')[-1]
    taste = callback.data.split('_')[-2]
    await state.update_data(volume=volume)
    await state.update_data(taste=taste)
    await callback.message.edit_text(text="""А теперь напишите дату начала приема в формате: 01-01-2025.""")
    await state.set_state(StateDrug.data_start)
    await callback.answer()


@router.message(F.text, StateFilter(StateDrug.data_start))
@error_handler
async def get_age(message: Message, state: FSMContext, bot: Bot):
    """
    Получаем дату начала приема препарата
    :param message:
    :param state:
    :param bot:
    :return:
    """
    logging.info('get_age')
    data_start_taking_drug = message.text
    if validate_date(data_start_taking_drug):
        year = int(data_start_taking_drug.split('-')[-1])
        month = int(data_start_taking_drug.split('-')[-2])
        day = int(data_start_taking_drug.split('-')[0])
        current_date = datetime.datetime.now()
        input_date = datetime.datetime(year=year, month=month, day=day)
        if current_date < input_date:
            await message.answer(text="Исходя из этих данных, сегодня у вас шестой день приема коллагена.\n"
                                      "Это верно или вы хотите заново указать дату начала приема препарата?",
                                 reply_markup=kb.keyboard_start_registration())
        elif current_date == input_date:
            await message.answer(text="Исходя из этих данных, вы хотите начать прием коллагена сегодня.\n"
                                      "Это верно или вы хотите заново указать дату начала приема препарата?",
                                 reply_markup=kb.keyboard_start_registration())
        else:
            await message.answer(text="Исходя из этих данных, вы хотите начать прием коллагена ДАТА в будущем.\n"
                                      "Это верно или вы хотите заново указать дату начала приема препарата?",
                                 reply_markup=kb.keyboard_start_registration())
        await state.update_data(data_start=data_start_taking_drug)
        start_day = current_date.day - input_date.day
        if start_day < 0:
            start_day = 0
        await state.update_data(start_day=start_day)
        await state.set_state(state=None)
    else:
        await message.answer(text='Укажите дату начала приема в формате: 01-01-2025.')


@router.callback_query(F.data.startswith('date_start_'))
@error_handler
async def date_start_taking_drug(callback: CallbackQuery, state: FSMContext, bot: Bot):
    """
    Получаем дату начала препарата
    :param callback: date_start_change
    :param state:
    :param bot:
    :return:
    """
    logging.info('date_start_taking_drug')
    action = callback.data.split('_')[-1]
    if action == 'change':
        await callback.message.edit_text(text="""Укажите дату начала приема в формате: 01-01-2025.""")
        await state.set_state(StateDrug.data_start)
    elif action == 'confirm':
        await callback.message.edit_text(text="📃Употреблять коллаген следует за 30 минут до еды один раз в день"
                                              " (утром, днем или вечером). В какое время вам будет удобно принимать"
                                              " коллаген? Введите свой ответ ниже в формате “10:00”")
        await state.set_state(StateDrug.time_start)


@router.message(F.text, StateFilter(StateDrug.time_start))
@error_handler
async def get_age(message: Message, state: FSMContext, bot: Bot):
    """
    Получаем удобное время для приема коллагена
    :param message:
    :param state:
    :param bot:
    :return:
    """
    logging.info('get_age')
    time_start_taking_drug = message.text
    if validate_time(time_start_taking_drug):
        await message.answer(text="Отлично! Спасибо, что указали все необходимые данные перед началом приема коллагена."
                                  " 😊Теперь я буду присылать вам сообщения, чтобы вам было удобно придерживаться"
                                  " графика приема препарата.\n"
                                  "Соблюдайте мои рекомендации и не забывайте, что за каждый своевременный прием вы"
                                  " будете получать бонусные баллы.")
        data = await state.get_data()
        start_day = data['start_day']
        current_hour = datetime.datetime.now().hour
        current_minute = datetime.datetime.now().minute
        current_date = datetime.datetime.now()
        year = int(data['data_start'].split('-')[-1])
        month = int(data['data_start'].split('-')[-2])
        day = int(data['data_start'].split('-')[0])
        drug_data = datetime.datetime(year=year, month=month, day=day)
        if current_date > drug_data and int(time_start_taking_drug.split(':')[0]) <= current_hour and int(time_start_taking_drug.split(':')[1]) < current_minute:
            start_day += 1
            await message.answer(text='Начнем присылать вам напоминания с завтрашнего дня,'
                                      ' надеюсь вы сегодня приняли коллаген самостоятельно.')
        data_drug = {
            "tg_id": message.from_user.id,
            "marketplace": data['marketplace'],
            "taste_drug": data['taste'],
            "volume_drug": data['volume'],
            "data_start_tacking": data['data_start'],
            "time_tacking": time_start_taking_drug,
            "start_day": data['start_day']
        }
        await rq.add_drug(data=data_drug)
    else:
        await message.answer(text="""Некорректно указано время. Введите свой ответ ниже в формате “10:00”""")
        await state.set_state(StateDrug.time_start)
