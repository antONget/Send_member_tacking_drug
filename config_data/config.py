from dataclasses import dataclass
from environs import Env


@dataclass
class TgBot:
    token: str
    admin_ids: str
    support_id: int
    group_id: str


@dataclass
class Test:
    test: str


@dataclass
class Config:
    tg_bot: TgBot
    test_bot: Test


def load_config(path: str = None) -> Config:
    env = Env()
    env.read_env(path)
    return Config(tg_bot=TgBot(token=env('BOT_TOKEN'),
                               admin_ids=env('ADMIN_IDS'),
                               support_id=env('SUPPORT_ID'),
                               group_id=env('GROUP_ID')),
                  test_bot=Test(test=env('TEST')))

