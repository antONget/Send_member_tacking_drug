from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup
from database.requests import UserRole
import logging


def keyboard_start() -> InlineKeyboardMarkup:
    logging.info("keyboard_start")
    button_1 = InlineKeyboardButton(text='Да', callback_data=f'start_yes')
    keyboard = InlineKeyboardMarkup(inline_keyboard=[[button_1]],)
    return keyboard


def keyboard_start_() -> ReplyKeyboardMarkup:
    logging.info("keyboard_start")
    button_1 = KeyboardButton(text='Препараты')
    button_2 = KeyboardButton(text='Оставить отзыв')
    keyboard = ReplyKeyboardMarkup(keyboard=[[button_1], [button_2]], resize_keyboard=True)
    return keyboard


def keyboard_start_admin() -> ReplyKeyboardMarkup:
    logging.info("keyboard_start")
    button_1 = KeyboardButton(text='Препараты')
    button_1 = KeyboardButton(text='Админ панель')
    keyboard = ReplyKeyboardMarkup(keyboard=[[button_1]], resize_keyboard=True)
    return keyboard
