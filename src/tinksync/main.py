from tinksync.tink import create_user, make_connect_bank_url, fetch_user_accounts, fetch_user_accounts, fetch_user_transactions
from tinksync.mongodb import get_user_settings, replace_user_settings, insert_user_settings
from tinksync import integrations

def cli_sync(username):
    user_settings = get_user_settings(username)
    if not user_settings:
        print("User does not exist!")
        return

    integration_settings = user_settings["integrations"]
    transactions = fetch_user_transactions(username)
    for integration_config in integration_settings:
        print(integration_config)
        integration_type = list(integration_config.keys())[0]
        integration_credentials = integration_config[integration_type]
        print(f"Syncing {integration_type}...")
        integration_class = integrations.__dict__.get(integration_type)
        integration_instance = integration_class(username, integration_credentials) # type: ignore
        integration_instance.reconciliate(transactions)

def cli_create(username):
    if get_user_settings(username):
        print("User already exists!")
        return
    
    create_user(username)
    new_record = {
        "username" : username
    }
    insert_user_settings(new_record)
    print("User created.")


def cli_get_accounts(username):
    user_settings = get_user_settings(username)
    if not user_settings:
        print("User does not exist!")
        return
    accounts = fetch_user_accounts(username)["accounts"]
    nicknames = user_settings["accountNicknames"]
    for account in accounts:
        nickname = nicknames.get(account["id"],  account["name"])
        balance_val = account["balances"]["booked"]["amount"]["value"]
        balance = float(balance_val["unscaledValue"]) / 10 ** int(balance_val["scale"])
        currency = account["balances"]["booked"]["amount"]["currencyCode"]
        print(f">> {account['id']} > {nickname} > {balance} {currency} > OK")

def cli_set_account_nickname(username, account_id, nickname):
    user_settings = get_user_settings(username)
    if not user_settings:
        print("User does not exist!")
        return

    user_settings["accountNicknames"][account_id] = nickname
    replace_user_settings(user_settings)

def cli_set_integration(username, integration_name, integration_settings):
    user_settings = get_user_settings(username)
    if not user_settings:
        print("User does not exist!")
        return

    user_settings['integrations'][integration_name] = integration_settings

def cli_get_transactions(username):
    user_settings = get_user_settings(username)
    if not user_settings:
        print("User does not exist!")
        return
    transactions = fetch_user_transactions(username)["transactions"]
    for transaction in transactions:
        amount_val = transaction["amount"]["value"]
        amount = float(amount_val["unscaledValue"]) / 10 ** int(amount_val["scale"])
        currency = transaction["amount"]["currencyCode"]
        description = transaction["descriptions"]["display"]
        date = transaction["dates"]["booked"]
        print(f">> {description} > {date} > {amount} {currency} ")
