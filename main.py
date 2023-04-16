def calculating(material_list):
    price = 0

    for material in material_list:
        *_, quantity, total_quantity, cost, _ = material
        material_price = cost / total_quantity * quantity
        price += material_price

    return price