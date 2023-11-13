from config import Config, load_config
from logics import pars_head_page, pars_categories_links, get_categories, pars_products


def main():
    '''Запуск скрипта'''

    #подгружаем данные о сайте подключения
    config: Config = load_config()
    headers = {'Accept': config.headers.accept, 'User-Agent': config.headers.user_agent}

    head_file = 'index.html'

    #парсим главную страницу
    pars_head_page(url=config.site.url, file_path=head_file, headers=headers)

    #парсим ссылки на категории товаров и сохраняем их в json
    categories_path = pars_categories_links(domain_name=config.site.domain, file_path=head_file)

    #достаем все категории из json документа
    all_categories = get_categories(categories_path)

    #парсим страницу с товарами и сохраняем их в 3-х форматах html, csv, json
    pars_products(all_categories, headers=headers)


if __name__ == '__main__':
    main()
