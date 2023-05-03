def calculating(material_list):
    price=0
    for material in material_list:
        quantity = material['quantity']
        total_quantity = material['total_quantity']
        material_price = material['price']
        price+= material_price/ total_quantity*quantity
    return price




