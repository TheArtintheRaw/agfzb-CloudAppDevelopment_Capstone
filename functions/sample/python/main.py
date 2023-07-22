"""IBM Cloud Function that gets all reviews for a dealership

Returns:
    List: List of reviews for the given dealership
"""
from ibmcloudant import CloudantV1
from ibm_cloud_sdk_core import IAMTokenManager
import requests


def main(param):
    """Main Function

    Args:
        param_dict (Dict): input paramater

    Returns:
        _type_: _description_ TODO
    """

    try:
        client = CloudantV1({
            account_name: param["COUCH_USERNAME"],
            api_key: param["IAM_API_KEY"],
            connect=True,
        })
        print(f"Databases: {client.all_dbs()}")
    except CloudantException as cloudant_exception:
        print("unable to connect")
        return {"error": cloudant_exception}
    except (requests.exceptions.RequestException, ConnectionResetError) as err:
        print("connection error")
        return {"error": err}

    return {"dbs": client.all_dbs()}
