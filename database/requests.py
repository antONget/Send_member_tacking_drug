from database.models import User, Drug, TakingDrug, FeedBack, Product, TackingDrugMessage, async_session
from sqlalchemy import select, update
import logging
from dataclasses import dataclass
from datetime import datetime


""" USER """


@dataclass
class UserRole:
    user = "user"
    executor = "executor"
    admin = "admin"
    partner = "partner"


async def add_user(data: dict) -> None:
    """
    Добавление пользователя
    :param data:
    :return:
    """
    logging.info(f'add_user')
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == data['tg_id']))
        if not user:
            session.add(User(**data))
            await session.commit()
        else:
            user.username = data['username']
            if data['qr']:
                user.qr = data['qr']
            await session.commit()


async def get_user_by_id(tg_id: int) -> User:
    """
    Получение информации о пользователе по tg_id
    :param tg_id:
    :return:
    """
    logging.info(f'get_user_by_id {tg_id}')
    async with async_session() as session:
        return await session.scalar(select(User).where(User.tg_id == tg_id))


async def get_user_registration(tg_id: int) -> bool:
    """
    Получение сведений о регистрации
    :param tg_id:
    :return:
    """
    logging.info('get_user_registration')
    async with async_session() as session:
        return await session.scalar(select(User).filter(User.tg_id == tg_id,
                                                         User.fullname == 'fullname'))


async def get_users() -> list[User]:
    """
    Получаем список пользователей принимающих препарат
    :return:
    """
    logging.info('get_user_registration')
    async with async_session() as session:
        users = await session.scalars(select(User))
        return [user for user in users]


async def set_user_full_name(tg_id: int, full_name: str) -> None:
    """
    Обновление имени пользователя
    :param tg_id:
    :param full_name:
    :return:
    """
    logging.info('set_user_full_name')
    async with async_session() as session:
        user = await session.scalar(select(User).filter(User.tg_id == tg_id))
        if user:
            user.fullname = full_name
            await session.commit()


async def set_user_age(tg_id: int, age: int) -> None:
    """
    Обновление имени пользователя
    :param tg_id:
    :param age:
    :return:
    """
    logging.info('set_user_age')
    async with async_session() as session:
        user = await session.scalar(select(User).filter(User.tg_id == tg_id))
        if user:
            user.age = age
            await session.commit()


async def set_user_balance(tg_id: int, balance: int) -> None:
    """
    Обновление баланса пользователя
    :param tg_id:
    :param balance:
    :return:
    """
    logging.info('set_user_balance')
    async with async_session() as session:
        user = await session.scalar(select(User).filter(User.tg_id == tg_id))
        if user:
            user.balance_user += balance
            await session.commit()


""" DRUG """


@dataclass
class StatusDrug:
    active = "active"
    completed = "completed"


async def add_drug(data: dict) -> None:
    """
    Добавление препарата
    :param data:
    :return:
    """
    logging.info(f'add_drug')
    async with async_session() as session:
        session.add(Drug(**data))
        await session.commit()


async def get_drug_id(drug_id: int) -> Drug:
    """
    Получаем препарат по его id
    :return:
    """
    logging.info('get_drug_id')
    async with async_session() as session:
        return await session.scalar(select(Drug).where(Drug.id == drug_id))


async def get_drugs() -> list[Drug]:
    """
    Получаем список пользователей принимающих препарат
    :return:
    """
    logging.info('get_drugs')
    async with async_session() as session:
        drugs = await session.scalars(select(Drug).where(Drug.status == StatusDrug.active))
        return [drug for drug in drugs]


async def get_drug_active_tg_id(tg_id: int) -> Drug:
    """
    Получаем список пользователей принимающих препарат
    :return:
    """
    logging.info('get_drug_active_tg_id')
    async with async_session() as session:
        return await session.scalar(select(Drug).filter(Drug.status == StatusDrug.active,
                                                        Drug.tg_id == tg_id))


async def get_drug_last_tg_id(tg_id: int) -> list[Drug]:
    """
    Получаем список пользователей принимающих препарат
    :return:
    """
    logging.info('get_drug_active_tg_id')
    async with async_session() as session:
        drugs = await session.scalars(select(Drug).where(Drug.tg_id == tg_id))
        return [drug for drug in drugs]


async def set_drug_balance(drug_id: int, balance: int) -> None:
    """
    Обновление баланса препарата
    :param drug_id:
    :param balance:
    :return:
    """
    logging.info('set_drug_balance')
    async with async_session() as session:
        drug = await session.scalar(select(Drug).filter(Drug.id == drug_id))
        if drug:
            drug.balance_drug += balance
            await session.commit()


async def set_drug_intake(drug_id: int, intake: int) -> None:
    """
    Обновление баланса препарата
    :param drug_id:
    :param intake:
    :return:
    """
    logging.info('set_drug_intake')
    async with async_session() as session:
        drug = await session.scalar(select(Drug).filter(Drug.id == drug_id))
        if drug:
            drug.drug_intake = intake
            await session.commit()


async def set_drug_time_tacking(drug_id: int, time_tacking: str) -> None:
    """
    Обновление баланса препарата
    :param drug_id:
    :param time_tacking:
    :return:
    """
    logging.info('set_drug_intake')
    async with async_session() as session:
        drug = await session.scalar(select(Drug).filter(Drug.id == drug_id))
        if drug:
            drug.time_tacking = time_tacking
            await session.commit()


async def set_drug_status(drug_id: int, status: str) -> None:
    """
    Обновление статуса приема препарата
    :param drug_id:
    :param status:
    :return:
    """
    logging.info('set_drug_intake')
    async with async_session() as session:
        drug = await session.scalar(select(Drug).filter(Drug.id == drug_id))
        if drug:
            drug.status = status
            await session.commit()


"""" TAKING_DRUG """


async def add_taking_drug(data: dict) -> None:
    """
    Добавление записи о приеме препарата
    :param data:
    :return:
    """
    logging.info(f'add_taking_drug')
    async with async_session() as session:
        session.add(TakingDrug(**data))
        await session.commit()


async def get_taking_drug_id(drag_id) -> list[TakingDrug]:
    """
    Получаем записи о приеме препарата по его id
    :return:
    """
    logging.info('get_taking_drug_id')
    async with async_session() as session:
        taking_drug = await session.scalars(select(TakingDrug).where(TakingDrug.drag_id == drag_id))
        return [t_d for t_d in taking_drug]


""" FEEDBACK """


async def add_feed_back(data: dict) -> None:
    """
    Добавление отзыва
    :param data:
    :return:
    """
    logging.info(f'add_feed_back')
    async with async_session() as session:
        session.add(FeedBack(**data))
        await session.commit()


""" PRODUCT """


async def add_product(data: dict) -> None:
    """
    Добавление препарата
    :param data:
    :return:
    """
    logging.info(f'add_product')
    async with async_session() as session:
        session.add(Product(**data))
        await session.commit()


async def get_products() -> list[Product]:
    """
    Получаем список продуктов
    :return:
    """
    logging.info('get_products')
    async with async_session() as session:
        products = await session.scalars(select(Product))
        return [product for product in products]


async def get_product_id(product_id: int) -> Product:
    """
    Получаем список продуктов
    :return:
    """
    logging.info('get_product_id')
    async with async_session() as session:
        return await session.scalar(select(Product).where(Product.id == product_id))


async def update_product(product_id: int, column: str, new_value: str) -> None:
    """
    Обновление поля
    :return:
    """
    logging.info('update_product')
    async with async_session() as session:
        await session.execute(update(Product).where(Product.id == product_id).values({column: new_value},))
        await session.commit()


async def select_value_product(product_id: int, column: str):
    """
    Получение значения определенного столбца продукта по его ID
    :param product_id: ID продукта
    :param column: имя столбца, который нужно выбрать
    :return: значение из столбца или None, если продукт не найден
    """
    logging.info(f'select_value_product called with product_id={product_id}, column={column}')

    if not hasattr(Product, column):  # Проверка, что колонка существует
        logging.error(f'Column {column} does not exist in Product model.')
        return None

    # Получение атрибута столбца через getattr
    column_attr = getattr(Product, column)

    async with async_session() as session:
        stmt = select(Product).where(Product.id == product_id).with_only_columns(column_attr)  # Передача атрибута напрямую
        result = await session.execute(stmt)
        value = result.scalars().first()
        return value


async def del_product(product_id: int) -> None:
    """
    Добавление препарата
    :param product_id:
    :return:
    """
    logging.info(f'add_product')
    async with async_session() as session:
        product = await session.scalar(select(Product).where(Product.id == product_id))
        if product:
            await session.delete(product)
            await session.commit()

""" TackingDrugMessage """


async def add_TackingDrugMessage(data: dict) -> None:
    """
    Добавление номера отправленного сообщения с напоминанием о приеме препарата
    :param data:
    :return:
    """
    logging.info(f'add_product')
    async with async_session() as session:
        row = await session.scalar(select(TackingDrugMessage).where(TackingDrugMessage.tg_id == data['tg_id']))
        if not row:
            session.add(TackingDrugMessage(**data))
            await session.commit()


async def get_TackingDrugMessage(tg_id: int) -> TackingDrugMessage:
    """
    Получение номера отправленного сообщения с напоминанием о приеме препарата
    :param tg_id:
    :return:
    """
    logging.info(f'add_product')
    async with async_session() as session:
        return await session.scalar(select(TackingDrugMessage).where(TackingDrugMessage.tg_id == tg_id))
