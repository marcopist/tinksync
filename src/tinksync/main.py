from tinksync import integrations
from tinksync.config import get_settings, set_settings
from tinksync.tink import create_user, fetch_user_accounts

class DupeUser(Exception):
    pass

class MissingUser(Exception):
    pass

def new_user_workflow(username):
    current_users = [record['username'] for record in get_settings()]

    if username in current_users:
        raise DupeUser
    
    resp = create_user(username)

    new_record = {
        "username" : username
    }
    set_settings(get_settings() + [new_record])

def accounts_user_workflow(username):
    current_users = [record['username'] for record in get_settings()]
    if username not in current_users:
        raise MissingUser
    accounts = fetch_user_accounts(username)

