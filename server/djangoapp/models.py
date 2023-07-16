"""
Model classes
"""

from django.db import models



class CarMake(models.Model):
    """
    Model representing a car make.
    """
    name = models.CharField(null=False, max_length=30)
    description = models.CharField(max_length=280)

    def __str__(self):
        return self.name


class CarModel(models.Model):
    """
    Model representing a car model.
    """
    # Constant for c_type choices
    TYPES = (
        ("SEDAN", "Sedan"),
        ("SUV", "SUV"),
        ("WAGON", "Wagon"),
        ("LIMOUSINE", "Limousine"),
        ("BATMOBILE", "Batmobile"),
    )

    make = models.ForeignKey(CarMake, on_delete=models.CASCADE)
    name = models.CharField(null=False, max_length=30)
    c_type = models.CharField(max_length=30, choices=TYPES)
    dealer_id = models.IntegerField()
    year = models.DateField()

    objects = models.Manager()

    def __str__(self):
        return f"Name: {self.name} Make Name: {self.make.name} Type: {self.c_type} Dealer ID: {self.dealer_id} Year: {self.year}"


class CarDealer:
    """
    Class representing car dealer data.
    """

    def __init__(self, address, city, full_name, id, lat, long, short_name, state, zip):
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
        self.state = state
        # Dealer zip
        self.zip = zip

    def __str__(self):
        return f"Dealer name: {self.full_name}"


class DealerReview:
    """
    Class representing dealer review data.
    """

    def __init__(self, dealership, name, purchase, review, purchase_date, car_make, car_model, car_year, sentiment, id):
        self.dealership = dealership
        self.name = name
        self.purchase = purchase
        self.review = review
        self.purchase_date = purchase_date
        self.car_make = car_make
        self.car_model = car_model
        self.car_year = car_year
        self.sentiment = sentiment  # Watson NLU service
        self.id = id

    def __str__(self):
        return f"Review: {self.review} Sentiment: {self.sentiment}"
