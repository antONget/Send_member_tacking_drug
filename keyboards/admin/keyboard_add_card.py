from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import logging


def keyboard_edit_card(product_id: int) -> InlineKeyboardMarkup:
    """
    Клавиатура для редактирования полей карточки
    :return:
    """
    logging.info("keyboard_edit_card")
    button_1 = InlineKeyboardButton(text=f'📸 Фото',
                                    callback_data=f'edit_card!photo!{product_id}')
    button_2 = InlineKeyboardButton(text=f'🗒 Название продукта',
                                    callback_data=f'edit_card!title_product!{product_id}')
    button_3 = InlineKeyboardButton(text=f'📄 Краткое описание',
                                    callback_data=f'edit_card!short_description!{product_id}')
    button_4 = InlineKeyboardButton(text=f'📑 Полное описание',
                                    callback_data=f'edit_card!full!{product_id}')
    button_5 = InlineKeyboardButton(text=f'🔗 Ссылки на товар',
                                    callback_data=f'edit_card!link!{product_id}')
    keyboard = InlineKeyboardMarkup(inline_keyboard=[[button_1], [button_2], [button_3], [button_4], [button_5]])
    return keyboard


def keyboard_edit_card_full(product_id: int) -> InlineKeyboardMarkup:
    """
    Клавиатура для редактирования полей карточки полного описания
    :return:
    """
    logging.info("keyboard_edit_card_full")
    button_1 = InlineKeyboardButton(text=f'💡Рекомендации по применению',
                                    callback_data=f'edit_card!full_description_use!{product_id}')
    button_2 = InlineKeyboardButton(text=f'⚠️Противопоказания',
                                    callback_data=f'edit_card!full_description_contraindications!{product_id}')
    button_3 = InlineKeyboardButton(text=f'📒Условия хранения',
                                    callback_data=f'edit_card!full_description_storage!{product_id}')
    button_4 = InlineKeyboardButton(text=f'🟡Состав',
                                    callback_data=f'edit_card!full_description_structure!{product_id}')
    button_5 = InlineKeyboardButton(text=f'💊Аминокислотный состав',
                                    callback_data=f'edit_card!full_description_aminoacid!{product_id}')
    keyboard = InlineKeyboardMarkup(inline_keyboard=[[button_1], [button_2], [button_3], [button_4], [button_5]])
    return keyboard


def keyboard_edit_card_link(product_id: int) -> InlineKeyboardMarkup:
    """
    Клавиатура для редактирования полей карточки ссылки
    :return:
    """
    logging.info("keyboard_edit_card_link")
    button_1 = InlineKeyboardButton(text=f'Сайт производителя',
                                    callback_data=f'edit_card!link_site!{product_id}')
    button_2 = InlineKeyboardButton(text=f'Озон',
                                    callback_data=f'edit_card!link_ozon!{product_id}')
    button_3 = InlineKeyboardButton(text=f'Вайлдберриз',
                                    callback_data=f'edit_card!link_wb!{product_id}')
    button_4 = InlineKeyboardButton(text=f'Яндекс.Маркет',
                                    callback_data=f'edit_card!link_ya!{product_id}')
    keyboard = InlineKeyboardMarkup(inline_keyboard=[[button_1], [button_2], [button_3], [button_4]])
    return keyboard
