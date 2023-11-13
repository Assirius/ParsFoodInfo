from environs import Env
from dataclasses import dataclass

env = Env()


@dataclass
class Headers:
    accept: str
    user_agent: str


@dataclass
class SiteInfo:
    url: str
    domain: str


@dataclass
class Config:
    headers: Headers
    site: SiteInfo


def load_config(path: str | None = None) -> Config:
    '''
    Функция возвращающая концифуграцию для подключения к сайту, url, headers, domain
    :param path: путь к файлу переменной окружения, где хранятся секретные данные
    :return: конфигурацию для подключения к сайту
    '''
    env.read_env(path)
    url = "https://health-diet.ru/table_calorie/?utm_source=leftMenu&utm_medium=table_calorie"
    domain_name = 'https://health-diet.ru'

    return Config(
        headers=Headers(
            accept=env('ACCEPT'),
            user_agent=env('USER-AGENT')
        ),
        site=SiteInfo(
            url=url,
            domain=domain_name
        ),
    )
