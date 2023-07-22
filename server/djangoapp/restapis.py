"""
_summary_

Returns:
_type_: _description_
"""
import json
import requests

from requests.auth import HTTPBasicAuth
from requests.exceptions import RequestException, Timeout, HTTPError, JSONDecodeError


from .models import CarDealer, DealerReview



def get_request(url, **kwargs):
    """
    Perform an HTTP GET request and return the JSON response.

    Args:
        url (str): The URL to make the GET request to.
        **kwargs: Additional keyword arguments that are passed as URL parameters.

    Returns:
        dict: A dictionary containing the JSON response data if the request is successful, None otherwise.
    """
    try:
        response = requests.get(url, headers={'Content-Type': 'application/json'}, params=kwargs, timeout=10)
        response.raise_for_status()  # Raise an exception for HTTP errors

        # Check if the response contains JSON data
        if response.headers.get('content-type') == 'application/json':
            json_data = response.json()
            return json_data
        else:
            print("Response does not contain JSON data.")
            return None

    except requests.exceptions.HTTPError as http_error:
        print("HTTP error:", http_error)
        print("Response text:", response.text)  # Print the response text for debugging
    except json.JSONDecodeError as json_error:
        print("JSON decoding error:", json_error)
    except requests.exceptions.RequestException as req_error:
        print("Request error:", req_error)

    return None  # Return None in case of an error



def post_request(url, payload, dealer_id=None, params=None, headers=None):
    """
    Perform an HTTP POST request and return the JSON response.

    Args:
        url (str): The URL to make the POST request to.
        payload (dict): The JSON payload to be sent in the request body.
        dealer_id (str, optional): The dealer ID parameter for the request (default: None).
        params (dict, optional): Additional URL parameters (default: None).
        headers (dict, optional): Additional headers for the request (default: None).

    Returns:
        dict: A dictionary containing the JSON response data if the request is successful, None otherwise.
    """
    try:
        response = requests.post(
            url,
            data=dealer_id,  # Change this to the correct parameter (data, json, or params)
            params=params,
            json=payload,
            headers=headers,
            timeout=10,
        )
        response.raise_for_status()  # Raise an exception for HTTP errors

        # Check if the response contains JSON data
        if response.headers.get('content-type') == 'application/json':
            json_data = response.json()
            return json_data
        else:
            print("Response does not contain JSON data.")
            return None

    except requests.exceptions.HTTPError as http_error:
        print("HTTP error:", http_error)
        print("Response text:", response.text)  # Print the response text for debugging
    except json.JSONDecodeError as json_error:
        print("JSON decoding error:", json_error)
    except requests.exceptions.RequestException as req_error:
        print("Request error:", req_error)

    return None  # Return None in case of an error

def get_dealers_from_cf(url, **kwargs):
    """
    Get a list of dealers from a cloud function and return a list of CarDealer objects.

    Args:
        url (str): The URL of the cloud function endpoint.
        **kwargs: Additional keyword arguments for URL parameters.

    Returns:
        list: A list of CarDealer objects containing dealer information.
    """
    results = []
    # Call get_request with a URL parameter
    json_result = get_request(url, **kwargs)
    if json_result and "rows" in json_result:
        # Get the row list in JSON as dealers
        dealers = json_result["rows"]
        # For each dealer object
        for dealer in dealers:
            if "doc" in dealer:
                dealer_doc = dealer["doc"]
                # Validate the presence of required keys and their data types
                if all(
                    key in dealer_doc and isinstance(dealer_doc[key], str)
                    for key in [
                        "address",
                        "city",
                        "full_name",
                        "dealer_id",
                        "lat",
                        "long",
                        "short_name",
                        "st",
                        "zip_code",
                    ]
                ):
                    # Create a CarDealer object with values in doc object
                    dealer_obj = CarDealer(
                        address=dealer_doc["address"],
                        city=dealer_doc["city"],
                        full_name=dealer_doc["full_name"],
                        dealer_id=dealer_doc["dealer_id"],
                        lat=dealer_doc["lat"],
                        long=dealer_doc["long"],
                        short_name=dealer_doc["short_name"],
                        st=dealer_doc["st"],
                        zip_code=dealer_doc["zip_code"],
                    )
                    results.append(dealer_obj)
                else:
                    print("Incomplete or invalid data for a dealer. Skipping.")
            else:
                print("Invalid JSON structure for a dealer. Skipping.")

    return results

def get_dealer_reviews_from_cf(url, dealer_id):
    """
    Get reviews by dealer id from a cloud function and return a list of DealerReview objects.
    """
    results = []

    # Include the dealer_id in the request URL or parameters as needed
    json_result = get_request(url, dealer_id=dealer_id)

    # Check if the JSON response is empty or not a dictionary
    if not json_result or not isinstance(json_result, dict):
        print("Invalid JSON response or empty data.")
        return results

    # Check if the key 'dealerships' exists in the JSON response
    if "dealerships" not in json_result:
        print("The key 'dealerships' is missing in the JSON response.")
        return results

    reviews = json_result["dealerships"]

    # Iterate over each review and validate the required fields
    for review in reviews:
        required_keys = ["id", "dealership", "name", "purchase", "review", "purchase_date", "car_make", "car_model", "car_year"]

        if not all(key in review for key in required_keys):
            print("Incomplete review data. Skipping this review.")
            continue

        # Extract review data from the JSON response
        review_id = review["id"]
        dealership = review["dealership"]
        name = review["name"]
        purchase = review["purchase"]
        review_text = review["review"]
        purchase_date = review["purchase_date"]
        car_make = review["car_make"]
        car_model = review["car_model"]
        car_year = review["car_year"]

        # Analyze review sentiment
        sentiment = analyze_review_sentiments(review_text)

        # Create a DealerReview object and append it to the results list
        review_obj = DealerReview(
            id=review_id,
            dealership=dealership,
            name=name,
            purchase=purchase,
            review=review_text,
            purchase_date=purchase_date,
            car_make=car_make,
            car_model=car_model,
            car_year=car_year,
            sentiment=sentiment,
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

    try:
        response = requests.post(
            nlu_url,
            data=params,
            headers={"Content-Type": "application/json"},
            auth=HTTPBasicAuth("apikey", api_key),
            timeout=10,
            **kwargs
        )
        response.raise_for_status()  # Raise an exception for 4xx and 5xx HTTP status codes
        sentiment = response.json()["sentiment"]["document"]["label"]
        return sentiment
    except Timeout:
        return "timeout_error"
    except HTTPError as http_err:
        return f"http_error: {http_err}"
    except JSONDecodeError as json_err:
        return f"json_decode_error: {json_err}"
    except RequestException as req_err:
        return f"request_exception: {req_err}"
