"""
views for django app
"""

import logging


from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.http import HttpResponse

from .restapis import get_dealers_from_cf, get_dealer_reviews_from_cf, post_request

# Get an instance of a logger
logger = logging.getLogger(__name__)


def about(request):
    """
    Renders the about page.

    :param request: HTTP request object
    :return: Rendered about page
    """
    context = {}
    if request.method == "GET":
        return render(request, 'djangoapp/about.html', context)


def contact(request):
    """
    Renders the contact page.

    :param request: HTTP request object
    :return: Rendered contact page
    """
    context = {}
    if request.method == "GET":
        return render(request, 'djangoapp/contact.html', context)


def login_request(request):
    """
    Handles the sign-in request.

    :param request: HTTP request object
    :return: Rendered index page or error message
    """
    context = {}
    url = "http://127.0.0.1:8000/djangoapp"
    dealerships = get_dealers_from_cf(url)
    context["dealership_list"] = dealerships

    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['pword']
        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            return render(request, 'djangoapp/index.html', context)
        else:
            context["message"] = "Username or password is incorrect."
            return render(request, 'djangoapp/index.html', context)
    else:
        return render(request, 'djangoapp/index.html', context)


def logout_request(request):
    """
    Handles the sign-out request.

    :param request: HTTP request object
    :return: Rendered index page
    """
    context = {}
    url = "https://us-south.functions.appdomain.cloud/api/v1/web/9cdefb68-1fae-422f-9f07-1688674cba78/api/get-dealerships"
    dealerships = get_dealers_from_cf(url)
    context["dealership_list"] = dealerships

    print(f"Log out the user `{request.user.username}`")
    logout(request)
    return render(request, 'djangoapp/index.html', context)


def registration_request(request):
    """
    _summary_

    Args:
        request (_type_): _description_

    Returns:
        _type_: _description_
    """
    context = {}
    # If it is a GET request, just render the registration page
    if request.method == 'GET':
        return render(request, 'djangoapp/registration.html', context)
    # If it is a POST request
    if request.method == 'POST':
        # Get user information from request.POST
        username = request.POST['username']
        password = request.POST['psw']
        first_name = request.POST['fname']
        last_name = request.POST['lname']
        user_exist = False
        try:
            # Check if user already exists
            User.objects.get(username=username)
            user_exist = True
        except Exception:
            # If not, simply log this is a new user
            logger.debug("%s is new user", User.username)
        # If it is a new user
        if not user_exist:
            # Create user in auth_user table
            user = User.objects.create_user(username=username, first_name=first_name, last_name=last_name, password=password)
            # Login the user and redirect to course list page
            login(request, user)
            return redirect("djangoapp:index")
        else:
            context["message"]="Account could not be created try again."
            return render(request, 'djangoapp/registration.html', context)

def get_dealerships(request):
    if request.method == "GET":
        url = "your-cloud-function-domain/dealerships/dealer-get"
        # Get dealers from the URL
        dealerships = get_dealers_from_cf(url)
        # Concat all dealer's short name
        dealer_names = ' '.join([dealer.short_name for dealer in dealerships])
        # Return a list of dealer short name
        return HttpResponse(dealer_names)


def get_dealer_details(request, dealer_id):
    """
    Renders the dealer details page with reviews.

    :param request: HTTP request object
    :param dealer_id: Dealer ID
    :return: Rendered dealer details page with reviews
    """
    context = {}
    url = "https://us-south.functions.appdomain.cloud/api/v1/web/9cdefb68-1fae-422f-9f07-1688674cba78/api/get-dealerships"

    dealer_details = get_dealer_reviews_from_cf(url, dealer_id)
    context["dealer_id"] = dealer_id
    context["reviews"] = dealer_details
    return render(request, 'djangoapp/dealer_details.html', context)


def add_review(request, dealer_id):
    """
    Handles the review submission.

    :param request: HTTP request object
    :param dealer_id: Dealer ID
    :return: Redirect to dealer details page or error message
    """
    context = {}

    if request.method == 'GET':
        url = "url"
        context = {
            "dealer_id": dealer_id,
            "dealer_name": get_dealers_from_cf(url)[dealer_id - 1].full_name,
        }
        return render(request, 'djangoapp/add_review.html', context)
    elif request.method == 'POST':
        if request.user.is_authenticated:
            review = {
                "id": 0,  # placeholder
                "name": request.POST["name"],
                "dealership": dealer_id,
                "review": request.POST["content"],
            }

            if "purchasecheck" in request.POST:
                review["purchase"] = True
                car_parts = request.POST["car"].split("|")
                review["purchase_date"] = request.POST["purchase_date"]
                review["car_make"] = car_parts[0]
                review["car_model"] = car_parts[1]
                review["car_year"] = car_parts[2]
            else:
                review["purchase"] = False
                review["purchase_date"] = None
                review["car_make"] = None
                review["car_model"] = None
                review["car_year"] = None

            try:
                json_result = post_request("url", review, dealer_id=dealer_id)

                if "error" in json_result:
                    context["message"] = "ERROR: Review was not submitted."
                else:
                    context["message"] = "Review was submitted."
            except Exception as error:
                logger.error("Error occurred while submitting review: {}".format(error))
                context["message"] = "ERROR: An error occurred while submitting the review."
        return redirect("djangoapp:dealer_details", dealer_id=dealer_id)