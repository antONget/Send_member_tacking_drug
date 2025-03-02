# from apscheduler.schedulers.asyncio import AsyncIOScheduler
# from utils.schedule_tacking_drug import mailing_list_users_scheduler
# from aiogram import Bot
#
# from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message
# from aiogram import Bot
# from datetime import datetime, timedelta
# from database import requests as rq
# from database.models import Drug, TakingDrug
# from utils.message_day_tacking_drug import message_day_volume
#
#
# async def mailing_list_users_scheduler(bot: Bot):
#     """
#     Получаем список пользователей, которые принимают препарат
#     :return:
#     """
#     list_drugs: list[Drug] = await rq.get_drugs()
#     current_hour = (datetime.now() + timedelta(hours=3)).second
#     for drug in list_drugs:
#         drug_hour = int(drug.time_tacking.split(':')[0])
#         print(current_hour, drug_hour)
#         if current_hour == drug_hour:
#             tacking_drugs: list[TakingDrug] = await rq.get_taking_drug_id(drag_id=drug.id)
#             day = drug.start_day + 1
#             if tacking_drugs:
#                 day += len(tacking_drugs)
#             dict_message: dict = await message_day_volume(day=day,
#                                                           volume=drug.volume_drug)
#             button = InlineKeyboardButton(text='Коллаген принят',
#                                           callback_data=f'collagen_{drug.id}')
#             keyboard = InlineKeyboardMarkup(inline_keyboard=[[button]])
#             msg = await bot.send_message(chat_id=drug.tg_id,
#                                          text=dict_message['message_day'],
#                                          reply_markup=keyboard)
#             scheduler = await scheduler_task_cron(bot=bot)
#             second = drug_hour + 10
#             scheduler.add_job(func=not_tacking_drag, trigger='cron', second=second,
#                               args=(msg, tacking_drugs, drug, bot,))
#
#
# async def not_tacking_drag(msg: Message, tacking_drugs: list[TakingDrug], drug: Drug, bot: Bot):
#     new_tacking_drugs: list[TakingDrug] = await rq.get_taking_drug_id(drag_id=drug.id)
#     print(len(new_tacking_drugs), len(tacking_drugs))
#     if len(new_tacking_drugs) == len(tacking_drugs):
#         await msg.delete()
#         data_taking_drug = {"tg_id": drug.tg_id,
#                             "drag_id": drug.id,
#                             "bonus": -10}
#         await rq.add_taking_drug(data=data_taking_drug)
#         await rq.set_user_balance(tg_id=drug.tg_id,
#                                   balance=-10)
#         await rq.set_drug_balance(drug_id=drug.id,
#                                   balance=-10)
#         tacking_drugs: list[TakingDrug] = await rq.get_taking_drug_id(drag_id=drug.id)
#         day = drug.start_day + 1
#         if tacking_drugs:
#             day += len(tacking_drugs)
#         dict_message: dict = await message_day_volume(day=day,
#                                                       volume=drug.volume_drug)
#         await bot.send_message(chat_id=drug.tg_id,
#                                text=dict_message['negative'])
#
#
# async def scheduler_task_cron(bot: Bot):
#     scheduler = AsyncIOScheduler(timezone="Europe/Moscow")
#     scheduler.add_job(func=mailing_list_users_scheduler, trigger='cron', second='*', args=(bot,))
#     scheduler.start()
#     return scheduler