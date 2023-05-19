from datetime import datetime
from typing import List, Dict, Tuple


def calculating(material_list: List[Dict]) -> float:
    """
    Подсчет себестоимости работы с помощью списка material_list.

    Вычисляется стоимость каждого материала по формуле:
        стоимость упаковки материала /общее количество материала в упаковке *количество требуемого материла.
    Стоимость каждого материала суммируется.

    :param material_list: Список материалов.
    :return: Себестоимость работы
    """
    price = 0
    for material in material_list:
        quantity = material['quantity']     # количество материала затраченное на изготовление работы
        total_quantity = material['total_quantity']     # общее количество материала в упаковке
        material_price = material['price']      # стоимость упаковки
        price += material_price / total_quantity*quantity
    return float("{:.2f}".format(price))


def date_format(date_str: str) -> str:
    """Изменение строки даты из формата бд в формат вывода на сайт.

    :param date_str: Дата в формате вывода из бд.
    :return: Дата в формате вывода на сайт.
    """
    date_time=datetime.strptime(date_str,'%Y-%m-%d %H:%M:%S.%f')
    format_datetime=date_time.strftime('%d %h %Y')
    return format_datetime


def prepare_handmade_list(handmade_list: List[Tuple]) -> List[Dict]:
    """
    Приводит полученный из бд список работ в необходимый для отображения на странице.

    :param handmade_list: Список кортежей с колонками из бд.
    :return: Список словарей с необходимыми ключами.
    """
    result = []

    for item in handmade_list:
        result.append({
            'id': item[0],
            'name': item[1],
            'link': item[5],
            'date_added': date_format(item[6]),
            'price': item[4],
            'user_name': item[3]
        })

    return result
