from typing import List, Dict


def calculating(material_list: List[Dict]):
    """
    Pасчет себестоимости работы с помощью списка material_list.

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
