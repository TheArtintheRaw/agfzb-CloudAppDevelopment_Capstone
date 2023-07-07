from django.db import models
from django.utils.timezone import now

class CarMake(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    # Add any other fields you'd like to include in the CarMake model

    def __str__(self):
        return self.name

class CarModel(models.Model):
    car_make = models.ForeignKey(CarMake, on_delete=models.CASCADE)
    dealer_id = models.IntegerField()
    name = models.CharField(max_length=100)
    TYPE_CHOICES = (
        ('sedan', 'Sedan'),
        ('suv', 'SUV'),
        ('wagon', 'Wagon'),
        # Add more choices as needed
    )
    type = models.CharField(max_length=10, choices=TYPE_CHOICES)
    year = models.DateField()
    # Add any other fields you'd like to include in the CarModel model

    def __str__(self):
        return self.name

class CarDealer:
    def __init__(self, address, city, full_name, id, lat, long, short_name, st, zip):
        # Dealer address
        self.address = address
        # Dealer city
        self.city = city
        # Dealer Full Name
        self.full_name = full_name
        # Dealer id
        self.id = id
        # Location lat
        self.lat = lat
        # Location long
        self.long = long
        # Dealer short name
        self.short_name = short_name
        # Dealer state
        self.st = st
        # Dealer zip
        self.zip = zip
    def __str__(self):
        return "Dealer name: " + self.full_name

class DealerReview(models.Model):
    dealership = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    purchase = models.CharField(max_length=100)
    review = models.TextField()
    purchase_date = models.DateField()
    car_make = models.CharField(max_length=100)
    car_model = models.CharField(max_length=100)
    car_year = models.IntegerField()
    sentiment = models.CharField(max_length=10)
    id = models.AutoField(primary_key=True)

    def __str__(self):
        return f"Review by {self.name} for {self.dealership}"