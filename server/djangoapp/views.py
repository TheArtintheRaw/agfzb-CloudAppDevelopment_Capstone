import json
import logging
from datetime import datetime
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
# from .models import related models
# from .restapis import related methods
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from .restapis import get_dealer_reviews_from_cf, post_request

# Get an instance of a logger
logger = logging.getLogger(__name__)


# Create your views here.

def base(request):
    context = {}
    if request.method == 'GET':
        return render(request, 'base.html', context)

def about(request):
    context = {}
    if request.method == 'GET':
        return render(request, 'djangoapp/about.html', context)


# Create a `contact` view to return a static contact page
def contact(request):
    context = {}
    if request.method == 'GET':
        return render(request, 'djangoapp/contact.html', context)

# Create a `login_request` view to handle sign in request
def login_request(request):
    context = {}
    # Handles POST request
    if request.method == "POST":
        # Get username and password from request.POST dictionary
        username = request.POST['username']
        password = request.POST['psw']
        # Try to check if provide credential can be authenticated
        user = authenticate(username=username, password=password)
        if user is not None:
            # If user is valid, call login method to login current user
            login(request, user)
            return redirect('djangoapp:index')
        else:
            # If not, return to login page again
            return render(request, 'djangoapp/login.html', context)
    else:
        return render(request, 'djangoapp/login.html', context)

# Create a `logout_request` view to handle sign out request
def logout_request(request):
    # Get the user object based on session id in request
    print("Log out the user `{}`".format(request.user.username))
    # Logout user in the request
    logout(request)
    # Redirect user back to course list view
    return redirect('djangoapp:index')

# Create a `registration_request` view to handle sign up request
def registration_request(request):
    context = {}
    # If it is a GET request, just render the registration page
    if request.method == 'GET':
        return render(request, 'djangoapp/registration.html', context)
    # If it is a POST request
    elif request.method == 'POST':
        # Get user information from request.POST
        username = request.POST['username']
        password = request.POST['psw']
        first_name = request.POST['firstname']
        last_name = request.POST['lastname']
        user_exist = False
        try:
            # Check if user already exists
            User.objects.get(username=username)
            user_exist = True
        except:
            # If not, simply log this is a new user
            logger.debug("{} is new user".format(username))
        # If it is a new user
        if not user_exist:
            # Create user in auth_user table
            user = User.objects.create_user(username=username, first_name=first_name, last_name=last_name,
                                            password=password)
            # Login the user and redirect to dealership
            login(request, user)
            return redirect("djangoapp:index")
        else:
            return render(request, 'djangoapp/registration.html', context)

# Update the `get_dealerships` view to render the index page with a list of dealerships
def get_dealerships(request):
    context = {}
    if request.method == "GET":
        return render(request, 'djangoapp/index.html', context)


# Create a `get_dealer_details` view to render the reviews of a dealer
# def get_dealer_details(request, dealer_id):
# ...

# Create a `add_review` view to submit a review
def add_review(request, dealer_id):
    context = {}
    if request.method == "GET":
        cars = query_cars_by_dealer(dealer_id)  # Assuming this function queries cars based on the dealer ID
        context['cars'] = cars
        return render(request, 'djangoapp/add_review.html', context)
    elif request.method == "POST":
        review = {
            "id": dealer_id,
            "name": request.user.username,
            "review": {
                "time": datetime.utcnow().isoformat(),
                "content": request.POST.get("content"),
                "purchase": request.POST.get("purchasecheck") == "on",
                "purchase_date": request.POST.get("purchasedate"),
                "car_make": request.POST.get("car_make"),
                "car_model": request.POST.get("car_model")
            }
        }
        json_payload = {"review": review}
        response = post_request(json_payload)  # Assuming this function sends the review data to the backend
        if response.status_code == 201:
            return redirect("djangoapp:dealer_details", dealer_id=dealer_id)
        else:
            return HttpResponse("Failed to add review.")

def get_dealer_details(request, dealer_id):
    context = {}
    reviews = get_dealer_reviews_from_cf(dealer_id)  # Assuming this function returns a list of reviews for the given dealer
    context['reviews'] = reviews
    return render(request, 'djangoapp/dealer_details.html', context)
