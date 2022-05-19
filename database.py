import sqlite3

from truck import Truck


class DatabaseCursor:
    def __init__(self, db_path):
        self.db_path = db_path
        self.connection = None

    def __enter__(self):
        self.connection = sqlite3.connect(self.db_path)
        return self.connection.cursor()

    def __exit__(self, exc_type, exc_value, exc_tb):
        self.connection.commit()
        self.connection.close()


def execute(command, db_path="trucks.db"):
    with DatabaseCursor(db_path) as cursor:
        cursor.execute(command)
        return cursor.fetchall()


def create_trucks_table(db_path="trucks.db"):
    command = """
    CREATE TABLE IF NOT EXISTS trucks_info (
    plate text PRIMARY KEY,
    model text NOT NULL,
    status bool NOT NULL,
    destination text NOT NULL);
    """
    execute(command, db_path=db_path)


def insert(*data, db_path="trucks.db", table="trucks_info"):
    command = f"""
    INSERT INTO {table}
    VALUES {data}
    """
    execute(command, db_path=db_path)


def select_all_trucks():
    return execute("select * from trucks_info")


def create_truck_from_data(data):
    truck = Truck()
    truck.plate = data[0]
    truck.name = data[1]
    truck.at_work = bool(data[2])
    truck.destination = data[3]
    return truck


def fetch_trucks_from_db():
    trucks_data = select_all_trucks()
    trucks = []
    for data in trucks_data:
        truck = create_truck_from_data(data)
        trucks.append(truck)
    return trucks


if __name__ == '__main__':
    create_trucks_table()
