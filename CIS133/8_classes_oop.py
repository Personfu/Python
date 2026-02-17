# ============================================================
# Classes & Object-Oriented Programming — Complete
# CIS 133 — Intro to Programming | Preston Furulie
# ============================================================
# Covers: classes, constructors, instance/class methods,
# properties, encapsulation, inheritance, polymorphism,
# abstract classes, magic methods, composition, and
# a full practical application.
# ============================================================

from abc import ABC, abstractmethod

print("=" * 60)
print("  CLASSES & OOP — CIS 133 | Preston Furulie")
print("=" * 60)


# ── Section 1: Basic Class with Constructor ─────────────────

class Student:
    """Represents a student with name, ID, and grades."""

    # Class variable (shared across all instances)
    school_name = "Portland Community College"
    student_count = 0

    def __init__(self, name, student_id):
        """Constructor: called when a new Student object is created."""
        self.name = name                  # instance variable
        self.student_id = student_id      # instance variable
        self._grades = []                 # protected (convention: single underscore)
        Student.student_count += 1        # increment class counter

    def add_grade(self, grade):
        """Add a grade (0-100) to the student's record."""
        if 0 <= grade <= 100:
            self._grades.append(grade)
        else:
            raise ValueError(f"Grade must be 0-100, got {grade}")

    def get_average(self):
        """Calculate the student's grade average."""
        if not self._grades:
            return 0.0
        return sum(self._grades) / len(self._grades)

    def get_letter_grade(self):
        """Convert numeric average to letter grade."""
        avg = self.get_average()
        if avg >= 90: return "A"
        if avg >= 80: return "B"
        if avg >= 70: return "C"
        if avg >= 60: return "D"
        return "F"

    @classmethod
    def get_student_count(cls):
        """Class method: accesses class variables, not instance variables."""
        return cls.student_count

    @staticmethod
    def is_passing(grade):
        """Static method: utility function that doesn't need self or cls."""
        return grade >= 70

    def __str__(self):
        """String representation for print()."""
        avg = self.get_average()
        return f"Student({self.name}, ID:{self.student_id}, Avg:{avg:.1f}, Grade:{self.get_letter_grade()})"

    def __repr__(self):
        """Developer representation for debugging."""
        return f"Student(name='{self.name}', id={self.student_id}, grades={self._grades})"

    def __eq__(self, other):
        """Equality comparison: two students are equal if they have the same ID."""
        if not isinstance(other, Student):
            return False
        return self.student_id == other.student_id

    def __lt__(self, other):
        """Less-than comparison: compare by average grade."""
        return self.get_average() < other.get_average()


print("\n--- Section 1: Basic Class ---")
s1 = Student("Preston Furulie", 10001)
s1.add_grade(95)
s1.add_grade(88)
s1.add_grade(92)
s1.add_grade(87)
print(f"  {s1}")
print(f"  School: {Student.school_name}")
print(f"  Is 75 passing? {Student.is_passing(75)}")


# ── Section 2: Properties (Getters/Setters) ─────────────────

class BankAccount:
    """Bank account with controlled access to balance via properties."""

    def __init__(self, owner, initial_balance=0):
        self.owner = owner
        self.__balance = initial_balance   # private (double underscore = name mangling)
        self.__transactions = []

    @property
    def balance(self):
        """Property getter: allows reading balance like an attribute."""
        return self.__balance

    @balance.setter
    def balance(self, value):
        """Property setter: validates before setting."""
        raise AttributeError("Cannot set balance directly. Use deposit/withdraw.")

    def deposit(self, amount):
        """Add money to the account."""
        if amount <= 0:
            raise ValueError("Deposit amount must be positive")
        self.__balance += amount
        self.__transactions.append(f"+${amount:.2f}")
        return self.__balance

    def withdraw(self, amount):
        """Remove money from the account."""
        if amount <= 0:
            raise ValueError("Withdrawal amount must be positive")
        if amount > self.__balance:
            raise ValueError("Insufficient funds")
        self.__balance -= amount
        self.__transactions.append(f"-${amount:.2f}")
        return self.__balance

    def get_statement(self):
        """Return formatted transaction history."""
        lines = [f"Account: {self.owner}", "-" * 30]
        for t in self.__transactions:
            lines.append(f"  {t}")
        lines.append(f"  {'Balance:':<20} ${self.__balance:.2f}")
        return "\n".join(lines)


print("\n--- Section 2: Properties & Encapsulation ---")
acct = BankAccount("Preston", 1000)
acct.deposit(500)
acct.deposit(250)
acct.withdraw(100)
print(acct.get_statement())
print(f"  Current balance: ${acct.balance:.2f}")


# ── Section 3: Inheritance ──────────────────────────────────

class Vehicle:
    """Base class for all vehicles."""

    def __init__(self, make, model, year, fuel_capacity):
        self.make = make
        self.model = model
        self.year = year
        self.fuel_capacity = fuel_capacity
        self.fuel_level = fuel_capacity
        self.odometer = 0
        self.speed = 0

    def accelerate(self, mph):
        """Increase speed."""
        self.speed = min(self.speed + mph, 200)

    def brake(self, mph):
        """Decrease speed."""
        self.speed = max(0, self.speed - mph)

    def drive(self, miles):
        """Drive a distance, consuming fuel."""
        fuel_needed = miles * self.fuel_consumption_rate()
        if fuel_needed > self.fuel_level:
            max_miles = self.fuel_level / self.fuel_consumption_rate()
            self.odometer += max_miles
            self.fuel_level = 0
            return f"Ran out of fuel after {max_miles:.1f} miles"
        self.fuel_level -= fuel_needed
        self.odometer += miles
        return f"Drove {miles} miles. Fuel: {self.fuel_level:.1f}gal"

    def fuel_consumption_rate(self):
        """Gallons per mile. Override in subclasses."""
        return 1 / 25  # default: 25 mpg

    def __str__(self):
        return (f"{self.year} {self.make} {self.model} | "
                f"{self.speed}mph | {self.odometer:.0f}mi | "
                f"Fuel: {self.fuel_level:.1f}gal")


class ElectricVehicle(Vehicle):
    """Electric vehicle: inherits from Vehicle, overrides fuel behavior."""

    def __init__(self, make, model, year, battery_kwh, range_miles):
        super().__init__(make, model, year, fuel_capacity=battery_kwh)
        self.battery_kwh = battery_kwh
        self.range_miles = range_miles

    def fuel_consumption_rate(self):
        """kWh per mile instead of gallons."""
        return self.battery_kwh / self.range_miles

    def charge(self, kwh):
        """Charge the battery."""
        self.fuel_level = min(self.battery_kwh, self.fuel_level + kwh)

    def __str__(self):
        pct = (self.fuel_level / self.battery_kwh) * 100
        return (f"{self.year} {self.make} {self.model} | "
                f"{self.speed}mph | {self.odometer:.0f}mi | "
                f"Battery: {pct:.0f}%")


class Truck(Vehicle):
    """Truck with towing capability and higher fuel consumption."""

    def __init__(self, make, model, year, fuel_capacity, tow_capacity_lbs):
        super().__init__(make, model, year, fuel_capacity)
        self.tow_capacity = tow_capacity_lbs
        self.is_towing = False

    def fuel_consumption_rate(self):
        """Trucks use more fuel; even more when towing."""
        base = 1 / 18  # 18 mpg
        return base * 1.4 if self.is_towing else base

    def hitch(self, weight):
        """Attach a load for towing."""
        if weight > self.tow_capacity:
            return f"Cannot tow {weight}lbs (max: {self.tow_capacity}lbs)"
        self.is_towing = True
        return f"Towing {weight}lbs"


print("\n--- Section 3: Inheritance ---")
sedan = Vehicle("Toyota", "Camry", 2024, 15.8)
sedan.accelerate(65)
print(f"  {sedan}")
print(f"  {sedan.drive(100)}")
print(f"  {sedan}")

print()
ev = ElectricVehicle("Tesla", "Model 3", 2025, 75, 350)
ev.accelerate(80)
print(f"  {ev}")
print(f"  {ev.drive(150)}")
print(f"  {ev}")

print()
truck = Truck("Ford", "F-150", 2024, 26, 13000)
print(f"  {truck.hitch(8000)}")
print(f"  {truck.drive(50)}")
print(f"  {truck}")


# ── Section 4: Polymorphism ─────────────────────────────────

print("\n--- Section 4: Polymorphism ---")
vehicles = [sedan, ev, truck]
for v in vehicles:
    # Same method call, different behavior based on type
    print(f"  {v.make} {v.model}: fuel rate = {v.fuel_consumption_rate():.4f} per mile")


# ── Section 5: Abstract Base Class ──────────────────────────

class Shape(ABC):
    """Abstract base class — cannot be instantiated directly.
    Subclasses MUST implement area() and perimeter()."""

    @abstractmethod
    def area(self):
        pass

    @abstractmethod
    def perimeter(self):
        pass

    def describe(self):
        return f"{self.__class__.__name__}: area={self.area():.2f}, perimeter={self.perimeter():.2f}"


class Circle(Shape):
    def __init__(self, radius):
        self.radius = radius

    def area(self):
        import math
        return math.pi * self.radius ** 2

    def perimeter(self):
        import math
        return 2 * math.pi * self.radius


class Rectangle(Shape):
    def __init__(self, width, height):
        self.width = width
        self.height = height

    def area(self):
        return self.width * self.height

    def perimeter(self):
        return 2 * (self.width + self.height)


class Triangle(Shape):
    def __init__(self, a, b, c):
        self.a = a
        self.b = b
        self.c = c

    def area(self):
        s = (self.a + self.b + self.c) / 2
        return (s * (s - self.a) * (s - self.b) * (s - self.c)) ** 0.5

    def perimeter(self):
        return self.a + self.b + self.c


print("\n--- Section 5: Abstract Classes ---")
shapes = [Circle(5), Rectangle(8, 4), Triangle(3, 4, 5)]
for shape in shapes:
    print(f"  {shape.describe()}")


# ── Section 6: Composition (Has-A Relationship) ─────────────

class Engine:
    def __init__(self, horsepower, fuel_type):
        self.horsepower = horsepower
        self.fuel_type = fuel_type
        self.running = False

    def start(self):
        self.running = True
        return f"{self.horsepower}hp {self.fuel_type} engine started"

    def stop(self):
        self.running = False
        return "Engine stopped"


class GPS:
    def __init__(self):
        self.latitude = 0.0
        self.longitude = 0.0

    def set_destination(self, lat, lon):
        self.latitude = lat
        self.longitude = lon
        return f"Navigating to ({lat}, {lon})"


class SmartCar:
    """Uses composition: SmartCar HAS-AN Engine and HAS-A GPS."""

    def __init__(self, name, hp, fuel):
        self.name = name
        self.engine = Engine(hp, fuel)      # composition
        self.gps = GPS()                    # composition

    def start_trip(self, lat, lon):
        results = []
        results.append(self.engine.start())
        results.append(self.gps.set_destination(lat, lon))
        return " | ".join(results)


print("\n--- Section 6: Composition ---")
car = SmartCar("Explorer", 300, "Hybrid")
print(f"  {car.start_trip(45.5155, -122.6789)}")
print(f"  Engine running: {car.engine.running}")


# ── Section 7: Full Practical Example ────────────────────────

print("\n--- Section 7: Complete Student Roster ---")
roster = [
    Student("Preston Furulie", 10001),
    Student("Alice Chen", 10002),
    Student("Bob Martinez", 10003),
    Student("Carol Williams", 10004),
]

# Add grades for each student
import random
random.seed(42)
for student in roster:
    for _ in range(5):
        student.add_grade(random.randint(65, 100))

# Sort by average (uses __lt__)
roster.sort(reverse=True)

print(f"\n  {'Rank':<6}{'Name':<22}{'Avg':>6}  {'Grade':>6}")
print("  " + "-" * 44)
for rank, student in enumerate(roster, 1):
    avg = student.get_average()
    letter = student.get_letter_grade()
    print(f"  {rank:<6}{student.name:<22}{avg:>6.1f}  {letter:>6}")

print(f"\n  Total students enrolled: {Student.get_student_count()}")
print(f"  School: {Student.school_name}")
