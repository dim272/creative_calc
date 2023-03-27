class Create:
    def __init__(self):
        self.name = self.get_name()
        self.materials = self.get_materials()

    def get_name(self):
        name = input('Как называется Ваша работа? ')
        return name

    def get_materials(self):
        materials = []
        while True:
            name = input('Как называется материал? ')
            count = input('Введите необходимое количество материала ? ')

            materials.append(
                {'name': name,
                 'count': count,

                 }

            )

            ask = input('Хотите ли Вы ввести следующий материал')
            if ask.lower() == 'нет':
                break
        return materials


class Calc:
    def __init__(self):
        self.name = self.get_name()
        self.quantity = self.get_quantity()

    def get_name(self):
        name = input('Какую работу подсчитать ? ')
        return name

    def get_quantity(self):
        quantity = input('Сколько Вы хотите подсчитать ? ')
        return quantity


class Delete:
    def get_objects(self):
        getobjectdel=input('Что Вы хотите удалить? ')
        return getobjectdel

    def choice_object(self):
        choiceobjectdel=input('Какое изделие Вы хотите выбрать? ')
        return choiceobjectdel

    def del_object(self):
        delobject=input('Вы действительно хотите удалить: "элемент"? ')


class Edit:
    def get_objects(self):
        getobjectedi = input('Что Вы хотите изменить? ')
        return getobjectedi

    def choice_object(self):
        choiceobjectedi= input('Какое изделие Вы хотите выбрать? ')
        return choiceobjectedi

    def get_materials(self):
        getmaterials=input('Выберите материал,который хотите изменить: ')

    def choice_material(self):
        pass

    def select_action(self):
        pass

    def edit_material(self):
        pass

    def del_material(self):
        pass

    def save_object(self):
        pass

