import json
class Cars:
    def __init__(self, brand, model, year, engine_volume, color, body_type, mileage, price):
        self.brand = brand
        self.model = model
        self.year = year
        self.engine_volume = engine_volume
        self.color = color
        self.body_type = body_type
        self.mileage = mileage
        self.price = price

class CreateMixin:
    cars = []

    def create(self, car):
        self.cars.append(car)
        return car

class ListingMixin:
    def listing(self):
        return self.cars

class RetrieveMixin:
    def retrieve(self, index):
        return self.cars[index]

class UpdateMixin:
    def update(self, index, car):
        self.cars[index] = car
        return car

class DeleteMixin:
    def delete(self, index):
        car = self.cars.pop(index)
        return car


class CarInventory(CreateMixin, ListingMixin, RetrieveMixin, UpdateMixin, DeleteMixin):
    def __init__(self, filename):
        self.filename = filename
        self.load_data()

    def create_car(self, brand, model, year, engine_volume, color, body_type, mileage, price):
        car = Cars(brand, model, year, engine_volume, color, body_type, mileage, price)
        self.create(car)
        self.save_data()
        return car

    def update(self, index, car):
        updated_car = super().update(index, car)
        self.save_data()
        return updated_car

    def delete(self, index):
        deleted_car = super().delete(index)
        self.save_data()
        return deleted_car

    def save_data(self):
        data = [vars(car) for car in self.listing()]
        with open(self.filename, 'w') as f:
            json.dump(data, f, indent=4)

    def load_data(self):
        try:
            with open(self.filename, 'r') as f:
                data = json.load(f)
                cars = [Cars(**car) for car in data]
                for car in cars:
                    self.create(car)
        except FileNotFoundError:
            pass
filename = 'car_inventory.json'
inventory = CarInventory(filename)

car1 = inventory.create_car('BMW', 'X5', 2022, 3.0, 'black', 'SUV', 100, 50000)
car2 = inventory.create_car('Audi', 'A6', 2021, 2.0, 'white', 'sedan', 50, 40000)
inventory.delete(0)
inventory.update(0, Cars('Audi', 'A7', 2023, 3.0, 'blue', 'coupe', 0, 60000))