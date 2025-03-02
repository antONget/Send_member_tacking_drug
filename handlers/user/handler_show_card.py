import datetime

from aiogram.types import CallbackQuery, Message
from aiogram import F, Router, Bot
from aiogram.fsm.context import FSMContext
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from keyboards.user import keyboard_main_menu as kb
from utils.error_handling import error_handler
from utils.utils_keyboard import utils_handler_pagination_one_card_photo_or_only_text
from config_data.config import Config, load_config
from database.models import Product
from database import requests as rq
import logging

router = Router()
config: Config = load_config()


class StateMainMenu(StatesGroup):
    change_time = State()


@router.message(F.text == 'Препараты')
@error_handler
async def process_product(message: Message, state: FSMContext, bot: Bot):
    """
    Показываем препараты
    :param message:
    :param state:
    :param bot:
    :return:
    """
    logging.info('process_product')
    products: list[Product] = await rq.get_products()
    print(products)
    await utils_handler_pagination_one_card_photo_or_only_text(list_items=products,
                                                               page=0,
                                                               text_button_select='Подробнее',
                                                               callback_prefix_select='show_product_select',
                                                               callback_prefix_back='show_product_back',
                                                               callback_prefix_next='show_product_next',
                                                               callback=None,
                                                               message=message)


@router.callback_query(F.data.startswith('show_product_'))
@error_handler
async def process_show_product(callback: CallbackQuery, state: FSMContext, bot: Bot):
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
        product: Product = await rq.get_product_id(product_id=product_id)
        photo = product.photo
        title_product = product.title_product
        dose_product = product.dose_product
        short_description = product.short_description
        full_description_use = product.full_description_use
        full_description_contraindications = product.full_description_contraindications
        full_description_storage = product.full_description_storage
        full_description_structure = product.full_description_structure
        full_description_aminoacid = product.full_description_aminoacid
        link_site = product.link_site
        link_wb = product.link_wb
        link_ya = product.link_ya
        link_ozon = product.link_ozon
        caption = f'<b>{title_product}</b>\n\n{short_description}\n{full_description_use}\n' \
                  f'{full_description_contraindications}\n{full_description_storage}\n{full_description_structure}\n' \
                  f'{full_description_aminoacid}\n' \
                  f'Ссылки на интернет-магазины\n\n' \
                  f'✅Где купить этот препарат:\n\n' \
                  f'<a href="{link_site}">Сайт производителя</a>\n' \
                  f'<a href="{link_wb}">Вайлдберрис</a>\n' \
                  f'<a href="{link_ya}">Яндекс.Маркет</a>\n' \
                  f'<a href="{link_ozon}">Озон</a>\n'
        await callback.message.answer(text=caption)
        return
    page = int(callback.data.split('_')[-1])
    products: list[Product] = await rq.get_products()
    await utils_handler_pagination_one_card_photo_or_only_text(list_items=products,
                                                               page=page,
                                                               text_button_select='Подробнее',
                                                               callback_prefix_select='show_product_select',
                                                               callback_prefix_back='show_product_back',
                                                               callback_prefix_next='show_product_next',
                                                               callback=callback,
                                                               message=None)