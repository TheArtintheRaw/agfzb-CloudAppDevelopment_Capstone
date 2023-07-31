from django.db import models
from django.utils.timezone import now

TYPES = {('Sedan', 'Sedan',), ('SUV', 'SUV'), ('HATCHBACK', 'HATCHBACK'), ('WAGON', 'WAGON')}

# <HINT> Create a Car Make model `class CarMake(models.Model)`:
class CarMake(models.Model):
    name = models.CharField(max_length=30)
    description = models.CharField(max_length=300)

    def __str__(self):
        return self.name

# <HINT> Create a Car Model model `class CarModel(models.Model):`:
class CarModel(models.Model):
    car_make = models.ForeignKey(CarMake, on_delete=models.CASCADE, related_query_name=CarMake.__name__)
    name = models.CharField(max_length=30)
    type_c = models.CharField(max_length=15, choices=TYPES)
    dealer_id = models.IntegerField()
    year = models.DateField()

    def __str__(self):
        return "Car Model: " + self.name


# <HINT> Create a plain Python class `CarDealer` to hold dealer data
class CarDealer:
    def __init__(self, id, address, city, state, st, zip, lat, long, short_name, full_name):
        self.id = id
        self.address = address
        self.city = city
        self.state = state
        self.st = st
        self.zip = zip
        self.lat = lat
        self.long = long
        self.short_name = short_name
        self.full_name = full_name

    def __str__(self):
        return "Dealer name: " + self.full_name

# <HINT> Create a plain Python class `DealerReview` to hold review data
class DealerReview:
    def __init__(self,
                review_id,
                name,
                dealership,
                purchase,
                review,
                purchase_date,
                car_make,
                car_model,
                car_year,
                sentiment):
        self.review_id = review_id
        self.name = name
        self.dealership = dealership
        self.purchase = purchase
        self.purchase_date = purchase_date
        self.review = review
        self.car_make = car_make
        self.car_model = car_model
        self.car_year = car_year
        self.sentiment = sentiment