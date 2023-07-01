"""API requests for setting up the Tink continuous transactions product.

This module implements the requests described in this document:
https://docs.tink.com/resources/transactions/continuous-connect-to-a-bank-account
"""

import os, requests, json

TINK_CLIENT_ID = os.environ.get('TINK_CLIENT_ID')
TINK_CLIENT_SECRET = os.environ.get('TINK_CLIENT_SECRET')


def _fetch_user_create_token():   # 1.1
    url = 'https://api.tink.com/api/v1/oauth/token'
    data = {
        'client_id': TINK_CLIENT_ID,
        'client_secret': TINK_CLIENT_SECRET,
        'grant_type': 'client_credentials',
        'scope': 'user:create'
    }
    response = requests.post(url, data=data)
    return response.json()['access_token']


def create_user(username):  # 1.2
    url = 'https://api.tink.com/api/v1/user/create'
    data = {
        'external_user_id': username,
        'market': 'GB',
        'locale': 'en_US'
    }
    headers = {
        'Authorization': f'Bearer {_fetch_user_create_token()}',
        'Content-Type': 'application/json'
    }
    response = requests.post(url, data=json.dumps(data), headers=headers)
    return response.json()

def _fetch_user_grant_token():  # 2.1
    url = 'https://api.tink.com/api/v1/oauth/token'
    data = {
        'client_id': TINK_CLIENT_ID,
        'client_secret': TINK_CLIENT_SECRET,
        'grant_type': 'client_credentials',
        'scope': 'authorization:grant'
    }
    response = requests.post(url, data=data)
    return response.json()['access_token']

def _fetch_authorization_code(username):  # 2.2
    url = 'https://api.tink.com/api/v1/oauth/authorization-grant/delegate'
    data = {
        'external_user_id': username,
        'id_hint': username,
        'actor_client_id': "df05e4b379934cd09963197cc855bfe9",
        'scope': 'authorization:read,authorization:grant,credentials:refresh,credentials:read,credentials:write,providers:read,user:read'
    }
    headers = {
        'Authorization': f'Bearer {_fetch_user_grant_token()}'
    }
    response = requests.post(url, data=data, headers=headers)
    return response.json()['code']

def make_connect_bank_url(username):  # 3
    authorization_code = _fetch_authorization_code(username)
    url = f'https://link.tink.com/1.0/transactions/connect-accounts?client_id={TINK_CLIENT_ID}&redirect_uri=https://console.tink.com/callback&authorization_code={authorization_code}&market=GB&locale=en_US'
    return url

def _fetch_user_auth_token(username):  # 4.1
    url = 'https://api.tink.com/api/v1/oauth/authorization-grant'
    data = {
        'external_user_id': username,
        'scope': 'accounts:read,balances:read,transactions:read,provider-consents:read'
    }
    headers = {
        'Authorization': f'Bearer {_fetch_user_grant_token()}'
    }
    response = requests.post(url, data=data, headers=headers)
    return response.json()['code']

def _fetch_user_access_token(username):  # 4.2
    url = 'https://api.tink.com/api/v1/oauth/token'
    data = {
        'client_id': TINK_CLIENT_ID,
        'client_secret': TINK_CLIENT_SECRET,
        'grant_type': 'authorization_code',
        'code': _fetch_user_auth_token(username)
    }
    response = requests.post(url, data=data)
    return response.json()['access_token']

def fetch_user_accounts(username):
    url = 'https://api.tink.com/api/v1/accounts/list'
    headers = {
        'Authorization': f'Bearer {_fetch_user_access_token(username)}'
    }
    response = requests.get(url, headers=headers)
    return response.json()

def fetch_user_transactions(username):
    url = 'https://api.tink.com/api/v2/transactions'
    headers = {
        'Authorization': f'Bearer {_fetch_user_access_token(username)}'
    }
    response = requests.get(url, headers=headers)
    return response.json()