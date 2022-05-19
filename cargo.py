from dataclasses import dataclass


@dataclass
class Cargo:
    weight: float
    length: float
    width: float
    height: float
    name: str = "Груз"

    def __post_init__(self):
        assert self.weight > 0, "Вес груза не может быть отрицательным или нулевым"
        assert self.length > 0, "Длина груза не может быть отрицательной или нулевой"
        assert self.width > 0, "Ширина груза не может быть отрицательной или нулевой"
        assert self.height > 0, "Высота груза не может быть отрицательной или нулевой"

    def get_volume(self):
        return self.length * self.width * self.height


if __name__ == '__main__':
    cargo = Cargo(1, 1, 0, 0)
