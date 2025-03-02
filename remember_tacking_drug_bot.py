from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from config_data.config import Config, load_config
from handlers import error, other_handlers, start_handler
from handlers.user import hundler_registration, hundler_add_drug, hundler_tacking_drug, hundler_feedback, \
    hundler_main_menu, handler_show_card
from handlers.admin import handler_edit_card, handler_add_card, handler_del_card, handler_feed_back
from notify_admins import on_startup_notify
from database.models import async_main
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from utils.schedule_tacking_drug import mailing_list_users_scheduler, not_tacking_collagen
import asyncio
import logging

logger = logging.getLogger(__name__)


# Функция конфигурирования и запуска бота
async def main():
    """
    Основной файл для запуска
    :return:
    """
    await async_main()
    # Конфигурируем логирование
    logging.basicConfig(
        level=logging.INFO,
        filename="py_log.log",
        filemode='w',
        format='%(filename)s:%(lineno)d #%(levelname)-8s '
               '[%(asctime)s] - %(name)s - %(message)s')

    # Выводим в консоль информацию о начале запуска бота
    logger.info('Starting bot')

    # Загружаем конфиг в переменную config
    config: Config = load_config()

    # Инициализируем бот и диспетчер
    bot = Bot(token=config.tg_bot.token, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    dp = Dispatcher()
    scheduler = AsyncIOScheduler(timezone="Europe/Moscow")
    if config.test_bot.test == 'TRUE':
        scheduler.add_job(func=mailing_list_users_scheduler, trigger='cron', second='*', args=(bot,))
        scheduler.add_job(func=not_tacking_collagen, trigger='cron', second='*', args=(bot,))
    else:
        scheduler.add_job(func=mailing_list_users_scheduler, trigger='cron', minute='*', args=(bot,))
        scheduler.add_job(func=not_tacking_collagen, trigger='cron', minute='*', args=(bot,))
    scheduler.start()
    await on_startup_notify(bot=bot)
    # Регистрируем router в диспетчере
    dp.include_router(error.router)
    dp.include_router(start_handler.router)
    dp.include_routers(handler_edit_card.router,
                       handler_add_card.router,
                       handler_del_card.router,
                       handler_feed_back.router)
    dp.include_routers(hundler_main_menu.router,
                       hundler_registration.router,
                       hundler_add_drug.router,
                       hundler_tacking_drug.router,
                       hundler_feedback.router,
                       handler_show_card.router)
    dp.include_router(other_handlers.router)

    # Пропускаем накопившиеся update и запускаем polling
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
