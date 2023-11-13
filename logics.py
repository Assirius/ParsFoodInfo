import os
import random
import time

import requests
from bs4 import BeautifulSoup

from services import open_file, normalize_name


def pars_head_page(url: str, file_path: str, headers: dict | None = None):
    '''
    Парсим и сохраняем главную страницу сайта

    :param url: url - главной страницы сайта
    :param file_path: путь до файла в который мы сохраним главную страницу
    :param headers: заголовки запросов
    '''

    req = requests.get(url, headers=headers)
    time.sleep(1)

    src = req.text
    open_file(path=file_path, mode='w', data=src)


def pars_categories_links(domain_name: str, file_path: str, path_dir='data'):
    '''
    Парсим ссылки на категории и сохраняем их в json файл

    :param domain_name: доменное имя сайта
    :param file_path: путь к файлу со страницей сайта с категориями продуктов
    :param: path_dir: дирректория в которую будут сохраняться данные (json документ по категориям)
    :return:
    '''

    domain_name = domain_name
    src = open_file(path=file_path)

    soup = BeautifulSoup(src, 'lxml')
    all_products_hrefs = soup.find_all(class_='mzr-tc-group-item-href')

    categories_dict = dict()
    for item in all_products_hrefs:
        item_text = item.text
        item_href = domain_name + item.get('href')

        categories_dict[item_text] = item_href

    categories_path = os.path.join(path_dir, 'categories.json')
    open_file(path=categories_path, mode='w', data=categories_dict)

    return categories_path


def get_categories(path_file: str):
    '''
    Поучаем json документ с категориями
    :param path_file: путь к файлу
    :return:
    '''
    all_categories = open_file(path=path_file)
    return all_categories


def add_product_headers(soup: BeautifulSoup, product_class: str, product_headers: dict[str, str]):
    '''
    :param soup: текст страницы с продуктами
    :param product_class: класс страницы в котором находятся заголовки
    :param product_headers: словарь с заголовками страницы
    '''
    if not product_headers:
        table_head = soup.find(class_=product_class).find('tr').find_all('th')
        product_headers.update({
            'title': table_head[0].string,
            'calories': table_head[1].string,
            'proteins': table_head[2].string,
            'fats': table_head[3].string,
            'carbohydrates': table_head[4].string,
        })


def get_product_info(item_row: BeautifulSoup) -> dict[str, str]:
    product_tds = item_row.find_all('td')
    product_row = {
            "Title": product_tds[0].find('a').string,
            "Calories": product_tds[1].string,
            "Proteins": product_tds[2].string,
            "Fats": product_tds[3].string,
            "Carbohydrates": product_tds[4].string
        }
    return product_row



def pars_products(all_categories: dict[str, str], headers: dict, path_dir='data'):
    '''
    Парсим страницу с продуктами по каждой категории, и сохраняем их в нашу дирректорию path_dir,
    Файлы будут сохранены в 3-х форматах, html, json, csv

    :param all_categories: славарь с ссылками на продукты по всем категориям
    :param headers: заголовки запросов
    :param path_dir: путь до дирректории куда будут сохранены наши файлы
    :return:
    '''

    product_headers = {}
    iteration_count = len(all_categories) - 1
    count = 0
    print(f'Всего итераций: {iteration_count}')
    for category_name, category_href in all_categories.items():

        category_name = normalize_name(string=category_name)

        #парсим страницу с продуктами по категории
        req = requests.get(url=category_href, headers=headers)
        src = req.text

        #путь куда будут сохранены все файлы с продуктами
        path_by_file = os.path.join(path_dir, f'{count}_{category_name}')

        # сохраняем html страницы с продуктами по каждой категории и работаем с сохраненнным файлом
        open_file(f'{path_by_file}.html', mode='w', data=src)
        src = open_file(f'{path_by_file}.html')

        soup = BeautifulSoup(src, 'lxml')
        product_class = 'mzr-tc-group-table'

        # проверка страницы на наличие таблицы с продуктами
        alert_block = soup.find(class_="uk-alert-danger")
        if alert_block is not None:
            continue

        #добавляе заголовки продуктов в словарь
        add_product_headers(soup=soup, product_class=product_class, product_headers=product_headers)

        #сохраняем заголовки в  .csv файл
        open_file(f'{path_by_file}.csv', mode='w', newline='', data=product_headers)


        # собираем данные по продуктам
        product_data = soup.find(class_=product_class).find('tbody').find_all('tr')

        product_info = []
        for item in product_data:
            #получаем данные о продукте
            product_dict = get_product_info(item)
            product_info.append(product_dict)

            #сохраняем данные о продукте в csv
            open_file(f'{path_by_file}.csv', mode='a', newline='', data=product_dict)


        #сохраняем данные о продукте в json документе
        open_file(f'{path_by_file}.json', mode='w', data=product_info)

        count += 1
        print(f'# Итерация {count}. {category_name}.csv записан')
        iteration_count -= 1

        if iteration_count == 0:
            print('Работа завершена!')
            break

        print(f'Осталось итераций:', iteration_count)
        time.sleep(random.randrange(2, 4))
