import database
from truck import Truck, TRUCKS
from cargo import Cargo


class CargoAccounting:
    def __init__(self):
        self._available_trucks = []
        self._trucks_at_work = []

        all_trucks = database.fetch_trucks_from_db()
        for truck in all_trucks:
            if truck.at_work:
                self._trucks_at_work.append(truck)
            else:
                self._available_trucks.append(truck)

    def add_truck(self, truck: Truck, generate_plate=True):
        assert isinstance(truck, Truck), "Машина должна быть класса Truck"

        other_trucks = database.fetch_trucks_from_db()
        if generate_plate:
            truck.generate_plate(other_trucks)

        database.insert(*truck.get_db_data(), table="trucks_info")

        self._available_trucks.append(truck) if not truck.at_work \
            else self._trucks_at_work.append(truck)

    def remove_truck(self, truck: Truck):
        assert isinstance(truck, Truck), "Машина должна быть класса Truck"
        database.execute(f"delete from trucks_info where plate='{truck.plate}'")
        if truck in self._available_trucks:
            self._available_trucks.remove(truck)
        elif truck in self._trucks_at_work:
            self._trucks_at_work.remove(truck)
        else:
            # print("not in trucks")
            pass

    def show_all_trucks(self):
        return self._available_trucks + self._trucks_at_work

    def show_available_trucks(self):
        return self._available_trucks

    def show_trucks_at_work(self):
        return self._trucks_at_work

    @staticmethod
    def sort_by_load_capacity(trucks, from_max=False):
        return sorted(trucks, key=lambda x: x.load_capacity, reverse=from_max)

    def show_trucks_sorted_by_load_capacity(self, from_max=False):
        all_trucks = self.show_all_trucks()
        return self.sort_by_load_capacity(all_trucks, from_max=from_max)

    def find_available_trucks(self, cargos):
        trucks = self.sort_by_load_capacity(self._available_trucks)
        truck_loads = [0 for _ in range(len(trucks))]
        for cargo in cargos:

            for i, truck in enumerate(trucks):
                if truck.load_capacity * 1000 >= cargo.weight and truck.holding_capacity >= cargo.get_volume():
                    truck.load_capacity -= cargo.weight / 1000
                    truck.holding_capacity -= cargo.get_volume()
                    # print(truck.load_capacity, truck.holding_capacity)
                    truck_loads[i] += 1
                    break

        return_trucks = [truck for i, truck in enumerate(trucks) if truck_loads[i]] \
            if sum(truck_loads) == len(cargos) else []

        if not return_trucks:
            for truck in trucks:
                truck.load_capacity = TRUCKS[truck.name.lower()]["грузоподъемность"]
                truck.holding_capacity = truck.get_volume()

        return return_trucks

    def request_transportation(self, cargos: list[Cargo], destination: str):
        assert all(isinstance(cargo, Cargo) for cargo in cargos), "Груз должен быть класса Cargo"
        available_trucks = self.find_available_trucks(cargos)
        if available_trucks:
            for truck in available_trucks:
                self.remove_truck(truck)
                truck.at_work = True
                truck.destination = destination
                self.add_truck(truck, generate_plate=False)
            return True
        return False


if __name__ == '__main__':
    account = CargoAccounting()
