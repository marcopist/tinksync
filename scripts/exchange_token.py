# scrpits/config.py looks like this, it is gitignored:
#     TOKENS = {
#         "monzo" : "token",
#         "revolut" : "token",
#         "american_express" : "token",
#         "starling" : "token",
#     }

#     CLIENT_ID = 'client_id'
#     CLIENT_SECRET = 'client_secret'


from .config import TOKENS, CLIENT_ID, CLIENT_SECRET
import requests


def exchange_token(token, client_id, client_secret):
    url = "https://api.tink.com/api/v1/oauth/token"
    data = {
        "code": token,
        "client_id": client_id,
        "client_secret": client_secret,
        "grant_type": "authorization_code",
    }
    response = requests.post(url, data=data)
    response.raise_for_status()
    return response.json()

if __name__ == "__main__":
    print(
        {
            bank : exchange_token(TOKENS[bank], CLIENT_ID, CLIENT_SECRET)
            for bank in TOKENS
        }
    )