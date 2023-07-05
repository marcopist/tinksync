import json, os

with open("settings.json", "r") as f:
    SETTINGS = json.loads(f.read())

TINK_CLIENT_ID = SETTINGS.get("tinkClientId", None)
TINK_CLIENT_SECRET = SETTINGS.get("tinkClientSecret", None)

_tink_accts = SETTINGS.get("tinkAccounts", None)

TINK_USERNAME = os.environ.get("TINK_USERNAME") or _tink_accts[0]["key"] if len(_tink_accts) > 0 else "myself"

DEBUG_MODE = SETTINGS.get("DEBUG_MODE", False)

TINK_USER = _tink_accts.get(TINK_USERNAME, None)


