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
from database.models import Product
from database import requests as rq
import logging

router = Router()
config: Config = load_config()


class StateAddCard(StatesGroup):
    photo = State()
    title_product = State()
    dose_product = State()
    short_description = State()
    full_description_use = State()
    full_description_contraindications = State()
    full_description_storage = State()
    full_description_structure = State()
    full_description_aminoacid = State()
    link_site = State()
    link_wb = State()
    link_ya = State()
    link_ozon = State()


@router.callback_query(F.data == 'action_add_card',)
@error_handler
async def process_add_product(callback: CallbackQuery, state: FSMContext, bot: Bot):
    """
    Добавление препарата
    :param callback:
    :param state:
    :param bot:
    :return:
    """
    logging.info('process_add_product')
    await state.set_state(state=None)
    await state.clear()
    await callback.message.edit_text(text='Пришлите название препарата')
    await state.set_state(StateAddCard.title_product)


@router.message(F.text, StateFilter(StateAddCard.title_product))
@error_handler
async def get_title_product(message: Message, state: FSMContext, bot: Bot):
    """
    Получаем название препарата
    :param message:
    :param state:
    :param bot:
    :return:
    """
    logging.info('get_title_product')
    title_product_ = message.html_text
    await state.update_data(title_product=title_product_)
    await message.answer(text='Пришлите фото продукта')
    await state.set_state(StateAddCard.photo)


@router.message(F.photo, StateFilter(StateAddCard.photo))
@error_handler
async def get_photo(message: Message, state: FSMContext, bot: Bot):
    """
    Получаем фото препарата
    :param message:
    :param state:
    :param bot:
    :return:
    """
    logging.info('get_photo')
    photo = message.photo[-1].file_id
    await state.update_data(photo=photo)
    await message.answer(text='Пришлите дозировку препарата')
    await state.set_state(StateAddCard.dose_product)


@router.message(F.text, StateFilter(StateAddCard.dose_product))
@error_handler
async def get_dose_product(message: Message, state: FSMContext, bot: Bot):
    """
    Получаем дозировку препарата
    :param message:
    :param state:
    :param bot:
    :return:
    """
    logging.info('get_dose_product')
    dose_product_ = message.text
    if dose_product_.isdigit() and 0 < int(dose_product_):
        await state.update_data(dose_product=int(dose_product_))
        await message.answer(text='Пришлите краткое описание препарата')
        await state.set_state(StateAddCard.short_description)
    else:
        await message.edit_text(text='Дозировка введена некорректна')


@router.message(F.text, StateFilter(StateAddCard.short_description))
@error_handler
async def get_short_description(message: Message, state: FSMContext, bot: Bot):
    """
    Получаем краткое описание препарата
    :param message:
    :param state:
    :param bot:
    :return:
    """
    logging.info('get_short_description')
    short_description_ = message.html_text
    await state.update_data(short_description=short_description_)
    await message.answer(text='Пришлите рекомендации по использованию препарата')
    await state.set_state(StateAddCard.full_description_use)


@router.message(F.text, StateFilter(StateAddCard.full_description_use))
@error_handler
async def get_full_description_use(message: Message, state: FSMContext, bot: Bot):
    """
    Получаем рекомендации по использованию препарата
    :param message:
    :param state:
    :param bot:
    :return:
    """
    logging.info('get_short_description')
    full_description_use_ = message.html_text
    await state.update_data(full_description_use=full_description_use_)
    await message.answer(text='Пришлите противопоказания для приема препарата')
    await state.set_state(StateAddCard.full_description_contraindications)


@router.message(F.text, StateFilter(StateAddCard.full_description_contraindications))
@error_handler
async def get_full_description_contraindications(message: Message, state: FSMContext, bot: Bot):
    """
    Получаем противопоказания препарата
    :param message:
    :param state:
    :param bot:
    :return:
    """
    logging.info('get_full_description_contraindications')
    full_description_contraindications_ = message.html_text
    await state.update_data(full_description_contraindications=full_description_contraindications_)
    await message.answer(text='Пришлите условия хранения и срок годности препарата')
    await state.set_state(StateAddCard.full_description_storage)


@router.message(F.text, StateFilter(StateAddCard.full_description_storage))
@error_handler
async def get_full_description_storage(message: Message, state: FSMContext, bot: Bot):
    """
    Получаем условия хранения и срок годности препарата
    :param message:
    :param state:
    :param bot:
    :return:
    """
    logging.info('get_full_description_storage')
    full_description_storage_ = message.html_text
    await state.update_data(full_description_storage=full_description_storage_)
    await message.answer(text='Пришлите состав препарата')
    await state.set_state(StateAddCard.full_description_structure)


@router.message(F.text, StateFilter(StateAddCard.full_description_structure))
@error_handler
async def get_full_description_storage(message: Message, state: FSMContext, bot: Bot):
    """
    Получаем условия хранения и срок годности препарата
    :param message:
    :param state:
    :param bot:
    :return:
    """
    logging.info('get_full_description_storage')
    full_description_structure_ = message.html_text
    await state.update_data(full_description_structure=full_description_structure_)
    await message.answer(text='Пришлите аминокислотный состав препарата')
    await state.set_state(StateAddCard.full_description_aminoacid)


@router.message(F.text, StateFilter(StateAddCard.full_description_aminoacid))
@error_handler
async def get_full_description_storage(message: Message, state: FSMContext, bot: Bot):
    """
    Получаем условия хранения и срок годности препарата
    :param message:
    :param state:
    :param bot:
    :return:
    """
    logging.info('get_full_description_storage')
    full_description_aminoacid_ = message.html_text
    await state.update_data(full_description_aminoacid=full_description_aminoacid_)
    await message.answer(text='Пришлите ссылку на покупку препарата на сайте производителя')
    await state.set_state(StateAddCard.link_site)


@router.message(F.text, StateFilter(StateAddCard.link_site))
@error_handler
async def get_link_site(message: Message, state: FSMContext, bot: Bot):
    """
    Получаем ссылку на покупку препарата на сайте производителя
    :param message:
    :param state:
    :param bot:
    :return:
    """
    logging.info('get_link_site')
    link_site_ = message.text
    await state.update_data(link_site=link_site_)
    await message.answer(text='Пришлите ссылку на покупку препарата на валдбериз')
    await state.set_state(StateAddCard.link_wb)


@router.message(F.text, StateFilter(StateAddCard.link_wb))
@error_handler
async def get_link_wb(message: Message, state: FSMContext, bot: Bot):
    """
    Получаем ссылку на покупку препарата на валдбериз
    :param message:
    :param state:
    :param bot:
    :return:
    """
    logging.info('get_link_wb')
    link_wb_ = message.text
    await state.update_data(link_wb=link_wb_)
    await message.answer(text='Пришлите ссылку на покупку препарата на Я.Маркете')
    await state.set_state(StateAddCard.link_ya)


@router.message(F.text, StateFilter(StateAddCard.link_ya))
@error_handler
async def get_link_ya(message: Message, state: FSMContext, bot: Bot):
    """
    Получаем ссылку на покупку препарата на озон
    :param message:
    :param state:
    :param bot:
    :return:
    """
    logging.info('get_link_ya')
    link_ya_ = message.text
    await state.update_data(link_ya=link_ya_)
    await message.answer(text='Пришлите ссылку на покупку препарата на OZON')
    await state.set_state(StateAddCard.link_ozon)


@router.message(F.text, StateFilter(StateAddCard.link_ozon))
@error_handler
async def get_link_ozon(message: Message, state: FSMContext, bot: Bot):
    """
    Получаем ссылку на покупку препарата на озон
    :param message:
    :param state:
    :param bot:
    :return:
    """
    logging.info('get_link_ozon')
    link_ozon_ = message.text
    await state.update_data(link_ozon=link_ozon_)
    await message.answer(text='Карточка препарата успешно добавлена')
    data = await state.get_data()
    await rq.add_product(data=data)
    await state.set_state(state=None)
