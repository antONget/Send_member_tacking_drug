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


@router.callback_query(F.data == 'action_del_card')
@error_handler
async def process_del_product(callback: CallbackQuery, state: FSMContext, bot: Bot):
    """
    Добавление препарата
    :param callback:
    :param state:
    :param bot:
    :return:
    """
    logging.info('process_del_product')
    products: list[Product] = await rq.get_products()
    if products:
        await utils_handler_pagination_one_card_photo_or_only_text(list_items=products,
                                                                   page=0,
                                                                   text_button_select='Удалить',
                                                                   callback_prefix_select='del_product_select',
                                                                   callback_prefix_back='del_product_back',
                                                                   callback_prefix_next='del_product_next',
                                                                   callback=callback,
                                                                   message=None)
    else:
        await callback.answer(text='Карточек для удаления нет', show_alert=True)


@router.callback_query(F.data.startswith('del_product_'))
@error_handler
async def process_delete_product(callback: CallbackQuery, state: FSMContext, bot: Bot):
    """
    Обработка действий показа продукта
    :param callback:
    :param state:
    :param bot:
    :return:
    """
    logging.info('process_show_product')
    if callback.data.split('_')[-2] == 'select':
        product_id = int(callback.data.split('_')[-1])
        await state.update_data(product_id=product_id)
        await callback.message.answer(text=f'Карточка препарата удалена')
        await rq.del_product(product_id=product_id)
        await callback.message.delete()
        return
    page = int(callback.data.split('_')[-1])
    products: list[Product] = await rq.get_products()
    await utils_handler_pagination_one_card_photo_or_only_text(list_items=products,
                                                               page=page,
                                                               text_button_select='Удалить',
                                                               callback_prefix_select='del_product_select',
                                                               callback_prefix_back='del_product_back',
                                                               callback_prefix_next='del_product_next',
                                                               callback=callback,
                                                               message=None)