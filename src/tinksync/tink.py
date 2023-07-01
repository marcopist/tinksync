"""API requests for setting up the Tink continuous transactions product.

This module implements the requests described in this document:
https://docs.tink.com/resources/transactions/continuous-connect-to-a-bank-account

scripts/cli.py is a CLI making use of these functions.
"""

import os, requests, json, curlify

TINK_CLIENT_ID = os.environ.get("TINK_CLIENT_ID")
TINK_CLIENT_SECRET = os.environ.get("TINK_CLIENT_SECRET")

def _debug(response):
    """Prints the request and response for debugging purposes."""
    print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
    print("--- Sent request ---")
    print(curlify.to_curl(response.request))

    print("--- Received response ---")
    print(response.json())
    print("<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<")


def _fetch_user_create_token(debug=False):
    """Step 1.1 in the Tink documentation."""
    url = "https://api.tink.com/api/v1/oauth/token"
    data = {"client_id": TINK_CLIENT_ID, "client_secret": TINK_CLIENT_SECRET, "grant_type": "client_credentials", "scope": "user:create"}
    response = requests.post(url, data=data)
    _debug(response) if debug else None
    return response.json()["access_token"]


def create_user(username, debug=False):
    """Step 1.2 in the Tink documentation.

    This function creates a Tink user with the given username.
    The API returns the Tink user ID, but this is not needed, as Tink will
    also accept the username as an identifier."""
    url = "https://api.tink.com/api/v1/user/create"
    data = {"external_user_id": username, "market": "GB", "locale": "en_US"}
    headers = {"Authorization": f"Bearer {_fetch_user_create_token()}", "Content-Type": "application/json"}
    response = requests.post(url, data=json.dumps(data), headers=headers)
    _debug(response) if debug else None
    return response.json()


def _fetch_user_grant_token(debug=False):
    """Step 2.1 in the Tink documentation."""
    url = "https://api.tink.com/api/v1/oauth/token"
    data = {
        "client_id": TINK_CLIENT_ID,
        "client_secret": TINK_CLIENT_SECRET,
        "grant_type": "client_credentials",
        "scope": "authorization:grant",
    }
    response = requests.post(url, data=data)
    _debug(response) if debug else None
    return response.json()["access_token"]


def _fetch_authorization_code(username, debug=False):
    """Step 2.2 in the Tink documentation."""
    url = "https://api.tink.com/api/v1/oauth/authorization-grant/delegate"
    data = {
        "external_user_id": username,
        "id_hint": username,
        "actor_client_id": "df05e4b379934cd09963197cc855bfe9",
        "scope": "authorization:read,authorization:grant,credentials:refresh,credentials:read,credentials:write,providers:read,user:read",
    }
    headers = {"Authorization": f"Bearer {_fetch_user_grant_token()}"}
    response = requests.post(url, data=data, headers=headers)
    _debug(response) if debug else None
    return response.json()["code"]


def make_connect_bank_url(username, debug=False):
    """Step 3 in the Tink documentation.

    This function returns a URL that the user should be redirected to.
    The user credentials will then be associated with the Tink user.
    """
    authorization_code = _fetch_authorization_code(username)
    url = f"https://link.tink.com/1.0/transactions/connect-accounts?client_id={TINK_CLIENT_ID}&redirect_uri=https://console.tink.com/callback&authorization_code={authorization_code}&market=GB&locale=en_US"
    return url


def _fetch_user_auth_token(username, debug=False):
    """Step 4.1 in the Tink documentation."""
    url = "https://api.tink.com/api/v1/oauth/authorization-grant"
    data = {"external_user_id": username, "scope": "accounts:read,balances:read,transactions:read,provider-consents:read"}
    headers = {"Authorization": f"Bearer {_fetch_user_grant_token()}"}
    response = requests.post(url, data=data, headers=headers)
    _debug(response) if debug else None
    return response.json()["code"]


def _fetch_user_access_token(username, debug=False):
    """Step 4.2 in the Tink documentation."""
    url = "https://api.tink.com/api/v1/oauth/token"
    data = {
        "client_id": TINK_CLIENT_ID,
        "client_secret": TINK_CLIENT_SECRET,
        "grant_type": "authorization_code",
        "code": _fetch_user_auth_token(username),
    }
    response = requests.post(url, data=data)
    _debug(response) if debug else None
    return response.json()["access_token"]


def fetch_user_accounts(username, debug=False):
    """Fetches the list of user accounts from the Tink API."""
    url = "https://api.tink.com/data/v2/accounts"
    headers = {"Authorization": f"Bearer {_fetch_user_access_token(username)}"}
    response = requests.get(url, headers=headers)
    _debug(response) if debug else None
    return json.dumps(response.json(), indent=2)


def fetch_user_transactions(username, debug=False):
    """Fetches the list of user transactions from the Tink API."""
    url = "https://api.tink.com/data/v2/transactions"
    headers = {"Authorization": f"Bearer {_fetch_user_access_token(username)}"}
    response = requests.get(url, headers=headers)
    _debug(response) if debug else None
    return json.dumps(response.json(), indent=2)
