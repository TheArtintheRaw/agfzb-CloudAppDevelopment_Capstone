"""
Model classes
"""

from django.db import models



class CarMake(models.Model):
    """_summary_

    Args:
        models (_type_): _description_

    Returns:
        _type_: _description_
    """
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return f'{self.name}'


class DealerReview(models.Model):
    """
    Class representing dealer review data.
    """

    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100)
    dealership = models.IntegerField()
    review = models.TextField()
    purchase = models.BooleanField()
    purchase_date = models.DateField()
    car_make = models.CharField(max_length=100)
    car_model = models.CharField(max_length=100)
    car_year = models.IntegerField()
    sentiment = models.CharField(max_length=100)

    def __str__(self):
        return f'Review: {self.review} Sentiment: {self.sentiment}'


class CarModel(models.Model):
    """_summary_

    Args:
        models (_type_): _description_

    Returns:
        _type_: _description_
    """
    TYPES = (
        ('SEDAN', 'Sedan'),
        ('SUV', 'SUV'),
        ('WAGON', 'Wagon'),
    )

    make = models.ForeignKey(CarMake, on_delete=models.CASCADE)
    dealer_id = models.IntegerField()
    name = models.CharField(max_length=100)
    c_type = models.CharField(max_length=100, choices=TYPES)
    year = models.IntegerField()
    reviews = models.ManyToManyField(DealerReview)

    def __str__(self):
        return f'{self.name} ({self.make})'


class CarDealer:
    """_summary_
    """
    def __init__(self, address, city, full_name, dealer_id, lat, long, short_name, st, zip_code):
        # Dealer address
        self.address = address
        # Dealer city
        self.city = city
        # Dealer Full Name
        self.full_name = full_name
        # Dealer id
        self.dealer_id = dealer_id
        # Location lat
        self.lat = lat
        # Location long
        self.long = long
        # Dealer short name
        self.short_name = short_name
        # Dealer state
        self.st = st
        # Dealer zip code
        self.zip_code = zip_code

    def __str__(self):
        return "Dealer name: " + self.full_name



