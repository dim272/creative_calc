from datetime import datetime
from typing import List, Dict, Tuple


def calculating(material_list: List[Dict]) -> int:
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
    return price


def date_format(date_str: str) -> str:
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
            'name': item[0],
            'link': '#',
            'date_added': date_format(item[1]),
            'price': item[2],
            'user_name': item[3]
        })

    return result
