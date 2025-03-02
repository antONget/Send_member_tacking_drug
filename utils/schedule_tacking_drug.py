import asyncio

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, InputMediaPhoto
from aiogram import Bot
from datetime import datetime, timedelta
from database import requests as rq
from database.models import Drug, TakingDrug, User, TackingDrugMessage
from utils.message_day_tacking_drug import message_day_volume
from config_data.config import Config, load_config

dict_message_edit = {}
config: Config = load_config()


async def mailing_list_users_scheduler(bot: Bot):
    """
    Получаем список пользователей, которые принимают препарат
    :return:
    """
    list_drugs: list[Drug] = await rq.get_drugs()
    # !!!!
    current_minute = (datetime.now()).minute
    current_hour = (datetime.now()).hour
    if config.test_bot.test == 'TRUE':
        current_hour = (datetime.now()).second % 30
    for drug in list_drugs:
        drug_hour = int(drug.time_tacking.split(':')[0])
        drug_minute = int(drug.time_tacking.split(':')[1])
        # print(f'{current_hour}:{current_minute}', f'{drug_hour}:{drug_minute}')
        tacking_drugs: list[TakingDrug] = await rq.get_taking_drug_id(drag_id=drug.id)
        CHECK = False
        if config.test_bot.test == 'TRUE':
            # print("1.TEST=TRUE", f'{current_hour}:{current_minute}', f'{drug_hour}:{drug_minute}')
            if current_hour == drug_hour:
                CHECK = True
        else:
            # print("1.TEST=FALSE", f'{current_hour}:{current_minute}', f'{drug_hour}:{drug_minute}')
            if drug_hour == current_hour and drug_minute == current_minute:
                CHECK = True
        if CHECK:
            day = drug.start_day + 1
            if tacking_drugs:
                day += len(tacking_drugs)
            dict_message: dict = await message_day_volume(day=day,
                                                          volume=drug.volume_drug)
            button = InlineKeyboardButton(text='Коллаген принят',
                                          callback_data=f'collagen_{drug.id}')
            keyboard = InlineKeyboardMarkup(inline_keyboard=[[button]])
            msg = await bot.send_photo(chat_id=drug.tg_id,
                                       photo=dict_message["image_id"],
                                       caption=f'<b>День: {day}.</b>\n\n'
                                               f'{dict_message["message_day"]}',
                                       reply_markup=keyboard)
            await rq.add_TackingDrugMessage(data={"tg_id": drug.tg_id,
                                                  "message_id": msg.message_id})
            dict_message_edit[drug.tg_id] = msg.message_id
            await rq.set_drug_intake(drug_id=drug.id,
                                     intake=0)


async def not_tacking_collagen(bot: Bot):
    list_drugs: list[Drug] = await rq.get_drugs()
    current_minute = (datetime.now()).minute
    current_hour = (datetime.now()).hour
    if config.test_bot.test == 'TRUE':
        current_hour = (datetime.now()).second % 30
    for drug in list_drugs:
        tacking_drug_message: TackingDrugMessage = await rq.get_TackingDrugMessage(tg_id=drug.tg_id)
        if not tacking_drug_message:
            continue
        # if not dict_message_edit.get(drug.tg_id, False):
        #     continue
        # print("not_tacking_collagen")
        drug_hour = int(drug.time_tacking.split(':')[0])
        drug_minute = int(drug.time_tacking.split(':')[1])
        # !!!!!
        CHECK = False
        if config.test_bot.test == 'TRUE':
            # print("2.TEST=TRUE", f'{current_hour}:{current_minute}', f'{drug_hour}:{drug_minute}')
            if current_hour == (drug_hour + 5):
                CHECK = True
        else:
            # print("2.TEST=FALSE", f'{current_hour}:{current_minute}', f'{drug_hour}:{drug_minute}')
            if (drug_hour + 1) == current_hour and drug_minute == current_minute:
                CHECK = True
        if CHECK:
            if not drug.drug_intake:
                info_user: User = await rq.get_user_by_id(tg_id=drug.tg_id)
                bonus = -10
                if info_user.balance_user <= 0:
                    bonus = 0
                data_taking_drug = {"tg_id": drug.tg_id,
                                    "drag_id": drug.id,
                                    "bonus": -10}
                await rq.add_taking_drug(data=data_taking_drug)
                await rq.set_user_balance(tg_id=drug.tg_id,
                                          balance=bonus)
                await rq.set_drug_balance(drug_id=drug.id,
                                          balance=-10)
                tacking_drugs: list[TakingDrug] = await rq.get_taking_drug_id(drag_id=drug.id)
                day = drug.start_day
                if tacking_drugs:
                    day += len(tacking_drugs)
                dict_message: dict = await message_day_volume(day=day,
                                                              volume=drug.volume_drug)

                await bot.edit_message_media(chat_id=drug.tg_id,
                                             media=InputMediaPhoto(media=dict_message["image_id"],
                                                                   caption=f'<b>День: {day}.</b>\n\n'
                                                                           f'{dict_message["negative"]}'),
                                             message_id=dict_message_edit[drug.tg_id],
                                             reply_markup=None)
                if drug.volume_drug == (drug.start_day + len(tacking_drugs)):
                    await rq.set_drug_status(drug_id=drug.id,
                                             status=rq.StatusDrug.completed)
                    button = InlineKeyboardButton(text='Оставить отзыв',
                                                  callback_data=f'feedback_{drug.id}')
                    keyboard = InlineKeyboardMarkup(inline_keyboard=[[button]])
                    await bot.send_message(chat_id=drug.tg_id,
                                           text='🤝Благодарю вас за выбор продукции PP Lab для укрепления и поддержки'
                                                ' своего здоровья. Если вы соблюдали все мои рекомендации и'
                                                ' придерживались графика, то уже могли заметить положительное'
                                                ' влияние коллагена на ваше внутреннее и внешнее состояние.\n\n'
                                                '<b>Мне бы хотелось узнать об этих изменениях. Почувствовали ли вы'
                                                ' прилив энергии, улучшилось ли состояние кожи или что-то еще приятно'
                                                ' вас удивило? Расскажите нам об этом.</b>\n\n'
                                                '1. Оставьте ваш отзыв о продукте на маркетплейсе,'
                                                ' где была совершена покупка.\n'
                                                '2. Пришлите сюда скриншот отзыва ⤵️\n'
                                                '3. В благодарность за уделенное время и ценную информацию вы получите'
                                                ' дополнительные бонусные баллы🎁.',
                                           reply_markup=keyboard)
