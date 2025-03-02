from sqlalchemy import String, Integer, DateTime, BigInteger, Boolean, Float
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine


engine = create_async_engine(url='sqlite+aiosqlite:///database/db.sqlite3')

async_session = async_sessionmaker(engine)


class Base(AsyncAttrs, DeclarativeBase):
    pass


class User(Base):
    __tablename__ = 'users'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    tg_id: Mapped[int] = mapped_column(BigInteger)
    username: Mapped[str] = mapped_column(String, default='username')
    qr: Mapped[str] = mapped_column(String, nullable=True)
    fullname: Mapped[str] = mapped_column(String, default='fullname')
    age: Mapped[int] = mapped_column(Integer, default=0)
    balance_user: Mapped[str] = mapped_column(Integer, default=0)


class Drug(Base):
    __tablename__ = 'dargs'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    tg_id: Mapped[int] = mapped_column(BigInteger)
    marketplace: Mapped[str] = mapped_column(String)
    taste_drug: Mapped[str] = mapped_column(String)
    volume_drug: Mapped[int] = mapped_column(Integer)
    data_start_tacking: Mapped[str] = mapped_column(String)
    time_tacking: Mapped[str] = mapped_column(String)
    start_day: Mapped[int] = mapped_column(Integer)
    drug_intake: Mapped[int] = mapped_column(Integer, default=0)
    status: Mapped[str] = mapped_column(String, default='active')
    balance_drug: Mapped[int] = mapped_column(Integer, default=0)


class TakingDrug(Base):
    __tablename__ = 'taking_drug'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    tg_id: Mapped[int] = mapped_column(BigInteger)
    drag_id: Mapped[int] = mapped_column(Integer)
    bonus: Mapped[int] = mapped_column(Integer)


class FeedBack(Base):
    __tablename__ = 'feed_back'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    tg_id: Mapped[int] = mapped_column(BigInteger)
    drug_id: Mapped[int] = mapped_column(Integer)
    feedback: Mapped[str] = mapped_column(String)


class Product(Base):
    __tablename__ = 'products'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    photo: Mapped[str] = mapped_column(String)
    title_product: Mapped[str] = mapped_column(String)
    dose_product: Mapped[str] = mapped_column(String)
    short_description: Mapped[str] = mapped_column(String)
    full_description_use: Mapped[str] = mapped_column(String)
    full_description_contraindications: Mapped[str] = mapped_column(String)
    full_description_storage: Mapped[str] = mapped_column(String)
    full_description_structure: Mapped[str] = mapped_column(String)
    full_description_aminoacid: Mapped[str] = mapped_column(String)
    link_site: Mapped[str] = mapped_column(String)
    link_wb: Mapped[str] = mapped_column(String)
    link_ya: Mapped[str] = mapped_column(String)
    link_ozon: Mapped[str] = mapped_column(String)


class TackingDrugMessage(Base):
    __tablename__ = 'tacking_drug_message'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    tg_id: Mapped[int] = mapped_column(BigInteger)
    message_id: Mapped[int] = mapped_column(Integer)


async def async_main():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


