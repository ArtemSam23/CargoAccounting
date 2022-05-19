from random import choices


TRUCKS = {
    "газель": {
        "грузоподъемность": 2.0,
        "длина": 3.0,
        "ширина": 2.0,
        "высота": 2.2,
        "фото": "pics/gazel.png"},

    "зил": {
        "грузоподъемность": 3.0,
        "длина": 5.0,
        "ширина": 2.2,
        "высота": 2.4,
        "фото": "pics/zil.png"},

    "man": {
        "грузоподъемность": 10.0,
        "длина": 8.0,
        "ширина": 2.45,
        "высота": 2.7,
        "фото": "pics/man.png"},

    "камаз": {
        "грузоподъемность": 20.0,
        "длина": 13.6,
        "ширина": 2.46,
        "высота": 2.7,
        "фото": "pics/kamaz.png"}}


class Truck:
    def __init__(self, name: str = "ГАЗель"):
        assert isinstance(name, str), "Пожалуйста, введите название в виде строки"
        assert name.lower() in TRUCKS.keys(), f"В нашей компании нет машин типа \"{name}\""

        self.plate = None
        self.name = name.upper()
        self.load_capacity = TRUCKS[name.lower()]["грузоподъемность"]
        self.length = TRUCKS[name.lower()]["длина"]
        self.width = TRUCKS[name.lower()]["ширина"]
        self.height = TRUCKS[name.lower()]["высота"]
        self.picture = TRUCKS[name.lower()]["фото"]
        self.holding_capacity = self.get_volume()

        self.at_work = False
        self.destination = "гараж"

    def get_volume(self):
        return round(self.length * self.width * self.height, 1)

    def __str__(self):
        return f"{self.name}; {'работает' if self.at_work else 'свободен'}; назначение: {self.destination}."

    def get_db_data(self):
        return self.plate, \
               self.name, \
               self.at_work, \
               self.destination

    def generate_plate(self, others):
        other_plates = [other.plate for other in others]
        chars = "".join(choices("АВЕКМНОРСТУХ", k=3))
        numbers = "".join(choices("0123456789", k=3))
        plate = chars[0] + numbers + chars[1:]

        if plate in other_plates:
            while plate in other_plates:
                plate = chars[0] + numbers + chars[1:]

        self.plate = plate
