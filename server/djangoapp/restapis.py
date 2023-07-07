import json
import requests
from django.shortcuts import render
from django.http import HttpResponse
from requests.auth import HTTPBasicAuth
from .models import CarDealer, DealerReview


def get_request(url, **kwargs):
    print(kwargs)
    print("GET from {} ".format(url))
    try:
        # Call get method of requests library with URL and parameters
        response = requests.get(url, headers={'Content-Type': 'application/json'},
                                    params=kwargs)
    except:
        # If any error occurs
        print("Network exception occurred")
    status_code = response.status_code
    print("With status {} ".format(status_code))
    json_data = json.loads(response.text)
    return json_data

def get_dealers_from_cf(url, **kwargs):
    results = []
    # Call get_request with a URL parameter
    json_result = get_request(url)
    if json_result:
        # Get the row list in JSON as dealers
        dealers = json_result["rows"]
        # For each dealer object
        for dealer in dealers:
            # Get its content in `doc` object
            dealer_doc = dealer["doc"]
            # Create a CarDealer object with values in `doc` object
            dealer_obj = CarDealer(address=dealer_doc["address"], city=dealer_doc["city"], full_name=dealer_doc["full_name"],
                                   id=dealer_doc["id"], lat=dealer_doc["lat"], long=dealer_doc["long"],
                                   short_name=dealer_doc["short_name"],
                                   st=dealer_doc["st"], zip=dealer_doc["zip"])
            results.append(dealer_obj)
    return results

def get_dealerships(request):
    if request.method == "GET":
        url = "https://us-east.functions.appdomain.cloud/api/v1/web/112d8330-f1d4-463f-a638-0d0e60e4bd65/dealership-package/get-dealership"
        # Get dealers from the URL
        dealerships = get_dealers_from_cf(url)
        # Concat all dealer's short name
        dealer_names = ' '.join([dealer.short_name for dealer in dealerships])
        # Return a list of dealer short name
        return HttpResponse(dealer_names)



def get_request(url, params=None, headers=None, auth=None):
    response = requests.get(url, params=params, headers=headers, auth=auth)
    return response

def post_request(url, params=None, json=None):
    response = requests.post(url, params=params, json=json)
    return response

def get_dealers_from_cf(url, **kwargs):
    response = get_request(url, **kwargs)
    if response.status_code == 200:
        dealers_data = response.json()
        # Parse JSON results into a CarDealer object list
        car_dealers = parse_car_dealers(dealers_data)
        return car_dealers
    else:
        print("Error retrieving dealers from Cloud Function.")
        return []

def get_dealer_reviews_from_cf(url, dealerId):
    params = {'dealerId': dealerId}
    response = get_request(url, params=params)
    if response.status_code == 200:
        reviews_data = response.json()
        # Parse JSON results into a DealerView object list
        dealer_reviews = parse_dealer_reviews(reviews_data)
        return dealer_reviews
    else:
        print("Error retrieving dealer reviews from Cloud Function.")
        return []

def analyze_review_sentiments(text):
    url = "https://your-watson-nlu-endpoint"  # Replace with your Watson NLU endpoint
    params = {'text': text, 'features': 'sentiment'}
    auth = HTTPBasicAuth('apikey', 'your-api-key')  # Replace with your Watson NLU API key
    headers = {'Content-Type': 'application/json'}
    response = get_request(url, params=params, headers=headers, auth=auth)
    if response.status_code == 200:
        analysis_data = response.json()
        sentiment = analysis_data['sentiment']['document']['label']
        return sentiment
    else:
        print("Error analyzing review sentiments.")
        return None



def get_dealer_reviews_from_cf(url, **kwargs):
    response = get_request(url, **kwargs)
    if response.status_code == 200:
        reviews_data = response.json()
        dealer_reviews = []

        for review_data in reviews_data:
            dealer_review = DealerReview(
                dealership=review_data['dealership'],
                name=review_data['name'],
                purchase=review_data['purchase'],
                review=review_data['review'],
                purchase_date=review_data['purchase_date'],
                car_make=review_data['car_make'],
                car_model=review_data['car_model'],
                car_year=review_data['car_year'],
                sentiment=review_data['sentiment'],
                id=review_data['id']
            )
            dealer_reviews.append(dealer_review)

        return dealer_reviews
    else:
        print("Error retrieving dealer reviews from Cloud Function.")
        return []

def get_dealer_details(request, dealer_id):
    url = "https://your-cloud-function-url"  # Replace with your cloud function URL
    dealer_reviews = get_dealer_reviews_from_cf(url, dealer_id)

    context = {
        'reviews': dealer_reviews,
    }

    return render(request, 'dealer_details.html', context)

# Create a `get_request` to make HTTP GET requests
# e.g., response = requests.get(url, params=params, headers={'Content-Type': 'application/json'},
#                                     auth=HTTPBasicAuth('apikey', api_key))


# Create a `post_request` to make HTTP POST requests
# e.g., response = requests.post(url, params=kwargs, json=payload)


# Create a get_dealers_from_cf method to get dealers from a cloud function
# def get_dealers_from_cf(url, **kwargs):
# - Call get_request() with specified arguments
# - Parse JSON results into a CarDealer object list


# Create a get_dealer_reviews_from_cf method to get reviews by dealer id from a cloud function
# def get_dealer_by_id_from_cf(url, dealerId):
# - Call get_request() with specified arguments
# - Parse JSON results into a DealerView object list


# Create an `analyze_review_sentiments` method to call Watson NLU and analyze text
# def analyze_review_sentiments(text):
# - Call get_request() with specified arguments
# - Get the returned sentiment label such as Positive or Negative



