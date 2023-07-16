"""
restapi structures
"""

import json
import requests

from requests.auth import HTTPBasicAuth
from requests.exceptions import RequestException, HTTPError
from .models import CarDealer, DealerReview

def get_request(url, params=None, headers=None, auth=None):
    """
    Make an HTTP GET request and return the JSON response.
    """
    json_data = {}
    try:
        response = requests.get(url, params=params, headers=headers, auth=auth, timeout=10)
        response.raise_for_status()  # Raise an exception for HTTP errors
        json_data = json.loads(response.text)
    except HTTPError as http_error:
        print("HTTP error:", http_error)
    except RequestException as request_error:
        print("Request error:", request_error)
    except json.JSONDecodeError as json_error:
        print("JSON decoding error:", json_error)
    except Exception as general_error:
        print("Error:", general_error)

    return json_data


def post_request(url, payload, dealer_id=None, params=None, headers=None):
    """
    Make an HTTP POST request and return the JSON response.
    """
    try:
        response = requests.post(url, dealer_id=dealer_id, params=params, json=payload, headers=headers, timeout=10)
        response.raise_for_status()  # Raise an exception for HTTP errors
    except HTTPError as http_error:
        print("HTTP error:", http_error)
    except RequestException as request_error:
        print("Request error:", request_error)
    except Exception as general_error:
        print("Error:", general_error)

    data = json.loads(response.text)
    return data


def get_dealers_from_cf(url, **kwargs):
    """
    Get dealers from a cloud function and return a list of CarDealer objects.
    """
    results = []
    json_result = get_request(url, **kwargs)
    if json_result:
        dealers = json_result["entries"]
        for dealer_doc in dealers:
            dealer_obj = CarDealer(
                address=dealer_doc["address"],
                city=dealer_doc["city"],
                full_name=dealer_doc["full_name"],
                id=dealer_doc["id"],
                lat=dealer_doc["lat"],
                long=dealer_doc["long"],
                short_name=dealer_doc["short_name"],
                state=dealer_doc["st"],
                zip=dealer_doc["zip"]
            )
            results.append(dealer_obj)

    return results


def get_dealer_reviews_from_cf(url, dealer_id):
    """
    Get reviews by dealer id from a cloud function and return a list of DealerReview objects.
    """
    results = []
    json_result = get_request(url, dealer_id)
    if "entries" in json_result:
        reviews = json_result["entries"]
        for review in reviews:
            review_obj = DealerReview(
                dealership=review["dealership"],
                name=review["name"],
                purchase=review["purchase"],
                review=review["review"],
                purchase_date=review["purchase_date"],
                car_make=review["car_make"],
                car_model=review["car_model"],
                car_year=review["car_year"],
                sentiment=analyze_review_sentiments(review["review"]),
                id=review["id"]
            )
            results.append(review_obj)

    return results


def analyze_review_sentiments(dealerreview, **kwargs):
    """
    Analyze the sentiment of a review using Watson NLU and return the sentiment label.
    """
    api_key = "BnxdV3tV6Ky1zhxc5VtDgrqmp5tfliBPLYh9pAQ_F5hW"
    nlu_url = "https://api.us-south.natural-language-understanding.watson.cloud.ibm.com/instances/a2a6abbb-1f03-48ac-896a-1c483b5370c3"
    params = json.dumps({"text": dealerreview, "features": {"sentiment": {}}})
    response = requests.post(nlu_url, data=params, headers={'Content-Type': 'application/json'},
                             auth=HTTPBasicAuth("apikey", api_key), timeout=10, **kwargs)

    try:
        sentiment = response.json()["sentiment"]["document"]["label"]
        return sentiment
    except Exception:
        return "neutral"
