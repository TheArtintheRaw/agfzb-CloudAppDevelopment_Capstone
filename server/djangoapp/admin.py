"""
python file containing admin classes
"""

# Temporary login credentials for reviewer:
# Username: root
# Password: root

from django.contrib import admin
from .models import CarMake, CarModel

# CarModelInline class
class CarModelInline(admin.StackedInline):
    """
    Inline admin class for CarModel model.
    """
    model = CarModel
    extra = 6

# CarModelAdmin class
class CarModelAdmin(admin.ModelAdmin):
    """
    Admin class for CarModel model.
    """
    list_display = ['name', 'dealer_id', 'c_type', 'year']
    search_fields = ['name']

# CarMakeAdmin class with CarModelInline
class CarMakeAdmin(admin.ModelAdmin):
    """
    Admin class for CarMake model.
    """
    inlines = [CarModelInline]
    list_display = ['name', 'description']
    search_fields = ['name']

# Register models here
admin.site.register(CarMake, CarMakeAdmin)
admin.site.register(CarModel)