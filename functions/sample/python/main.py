"""IBM Cloud Function that gets all reviews for a dealership

Returns:
    List: List of reviews for the given dealership
"""
from ibmcloudant.cloudant_v1 import CloudantV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
import requests

authenticator = IAMAuthenticator('{apikey}')

service = CloudantV1(authenticator=authenticator)

service.set_service_url('{url}')

def main():

    response = service.post_all_docs(
        db='dealerships',
        include_docs=True,
        limit=10
    ).get_result()

    print(response)
