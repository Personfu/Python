# Classes & Object-Oriented Programming
# CIS 133 — Intro to Programming | Preston Furulie

class Vehicle:
    def __init__(self, make, model, year):
        self.make = make
        self.model = model
        self.year = year
        self.speed = 0

    def accelerate(self, amount):
        self.speed += amount

    def brake(self, amount):
        self.speed = max(0, self.speed - amount)

    def __str__(self):
        return f"{self.year} {self.make} {self.model} ({self.speed} mph)"


class ElectricVehicle(Vehicle):
    def __init__(self, make, model, year, battery_kwh):
        super().__init__(make, model, year)
        self.battery_kwh = battery_kwh
        self.charge = 100

    def drive(self, miles):
        drain = miles * 0.3
        self.charge = max(0, self.charge - drain)

    def __str__(self):
        base = super().__str__()
        return f"{base} | Battery: {self.charge:.0f}%"


# Test the classes
car = Vehicle("Toyota", "Camry", 2024)
car.accelerate(60)
print(car)
car.brake(20)
print(car)
print()

ev = ElectricVehicle("Tesla", "Model 3", 2025, 75)
ev.accelerate(80)
ev.drive(50)
print(ev)
ev.drive(100)
print(ev)
