"""
Sample module to demonstrate how to consume the GraspDP Storage API.

Example response payload (products data):
[
    {
        "allowPosting": false,
        "averagePrice": 0.0,
        "code": "09-001",
        "costPrice": 0.0,
        "createdAt": 1158785400000,
        "currency_dbId": null,
        "dateLimit": false,
        "dbId": 1915441,
        "description": "Reiseutlegg",
        "exchangeRate": 0.0,
        "expenses": false,
        "fileFile_dbId": null,
        "flexiFieldsItem_code1_dbId": null,
        ...,  # Other fields
        "_uid": "1915441",
        "id": 0,
        "_tenant_id": "eae3b2be-f377-445e-86b0-ead33827daae",
        "_owner_id": "38450772",
        "_source_time": null,
        "_system_time": 1718022344074,
        "_valid_from": 1718022344074,
        "_valid_to": null,
        "_id_range": "0-9999"
    }
    ...
]
"""

import base64
import json
import os
import typing

import requests


def get_basic_auth_header(client_id, client_secret) -> dict:
    """
    Return a dict containing the correct headers to set to make HTTP Basic
    Auth request
    @param client_id: client_id
    @param client_secret: client_secret
    @return: dict
    """
    user_pass = "{0}:{1}".format(client_id, client_secret)
    auth_string = base64.b64encode(user_pass.encode("utf-8"))
    auth_headers = {
        "AUTHORIZATION": "Basic " + auth_string.decode("utf-8"),
    }
    return auth_headers


def get_auth_header(
    url: str,
    client_id: str,
    client_secret: str,
) -> typing.Dict:
    """
    Function returning JWT token Auth Header OAuth2 client credentials flow.
    @param url: url
    @param client_id: client_id
    @param client_secret: client_secret
    @return: str
    """
    token_request_data = {
        "grant_type": "client_credentials",
    }
    auth_headers = get_basic_auth_header(
        client_id, client_secret
    )

    response = requests.post(
        url, data=token_request_data, headers=auth_headers
    )

    if response.status_code != 200:
        raise PermissionError(f"Failed to get JWT token: {response.content}")

    print("Authentication successful")

    identity_payload = json.loads(response.content.decode("utf-8"))
    return {"Authorization": f"Bearer {identity_payload['access_token']}"}


def fetch(
    url: str,
    headers: typing.Dict,
    params: typing.Dict,
) -> requests.Response:
    """
    Function to submit data to API.
    @param url: url
    @param headers: headers
    @param data: data
    @return: requests.Response
    """
    return requests.get(url, params=params, headers=headers)


if __name__ == "__main__":
    """
    Example of fetching data from API.
    """

    CLIENT_ID = os.environ.get("CLIENT_ID")
    CLIENT_SECRET = os.environ.get("CLIENT_SECRET")
    LOGIN_URL = "https://auth.grasp-daas.com/oauth/token/"
    SUBMIT_URL = "https://grasp-daas.com/api/storage/v1/submit/"

    data = [{}]
    auth_headers = get_auth_header(
        url=LOGIN_URL,
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
    )

    extra_headers = {"Content-Type": "application/json"}

    headers = {**auth_headers, **extra_headers}

    params = {
        "source_system": "xledger",
        "dataset": "products",
        "source_id": "38450772",
        "workspace": "cart"
    }

    response = fetch(
        url=SUBMIT_URL,
        headers=headers,
        params=params,
    )
    print(response, response.json())
