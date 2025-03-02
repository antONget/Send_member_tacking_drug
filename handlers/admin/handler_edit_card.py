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


class StateEditCard(StatesGroup):
    edit_column = State()


@router.message(F.text == 'Админ панель', IsSuperAdmin())
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
    await message.answer(text='Выберите действие с карточкой препарата',
                         reply_markup=kb.keyboard_action_card())


@router.callback_query(F.data == 'action_edit_card',)
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
    products: list[Product] = await rq.get_products()
    if products:
        await utils_handler_pagination_one_card_photo_or_only_text(list_items=products,
                                                                   page=0,
                                                                   text_button_select='Подробнее',
                                                                   callback_prefix_select='edit_product_select',
                                                                   callback_prefix_back='edit_product_back',
                                                                   callback_prefix_next='edit_product_next',
                                                                   callback=callback,
                                                                   message=None)
    else:
        await callback.answer(text='Карточек для редактирования нет', show_alert=True)


@router.callback_query(F.data.startswith('edit_product_'))
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
        await state.update_data(product_id=product_id)
        product: Product = await rq.get_product_id(product_id=product_id)
        await callback.message.delete()
        await callback.message.answer(text=f'<b>{product.title_product}</b>\n\n'
                                           f'Выберите поле карточки продукта для редактирования',
                                      reply_markup=kb.keyboard_edit_card(product_id=product_id))
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


@router.callback_query(F.data.startswith('edit_card'))
@error_handler
async def process_edit_card(callback: CallbackQuery, state: FSMContext, bot: Bot):
    """

    :param callback:
    :param state:
    :param bot:
    :return:
    """
    logging.info('process_edit_card')
    product_id = int(callback.data.split('!')[-1])
    column = callback.data.split('!')[-2]
    if column == 'full':
        pass
        return
    elif column == 'link':
        pass
        return
    print(column, product_id)
    value = await rq.select_value_product(product_id=product_id, column=column)

    await state.update_data(column_edit=column)
    await callback.message.edit_text(text=f'{value}\n\n'
                                          f'Пришлите новое значение')
    await state.set_state(StateEditCard.edit_column)


@router.message(StateFilter(StateEditCard.edit_column))
@error_handler
async def process_edit_column(message: Message, state: FSMContext, bot: Bot):
    """
    Обновление поля карточки
    :param message:
    :param state:
    :param bot:
    :return:
    """
    logging.info('process_edit_column')
    new_value = message.html_text
    if message.photo:
        new_value = message.photo[-1].file_id
    data = await state.get_data()
    product_id = data['product_id']
    column = data['column_edit']
    await rq.update_product(product_id=product_id, column=column, new_value=new_value)
    product: Product = await rq.get_product_id(product_id=product_id)
    await message.answer(text=f'<b>{product.title_product}</b>\n\n'
                              f'Выберите поле карточки продукта для редактирования',
                         reply_markup=kb.keyboard_edit_card(product_id=product_id))
