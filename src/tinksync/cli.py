#!usr/bin/env python

"""This module contains a CLI which can be used to create a Tink user, generate a bank connection URL, and fetch the accounts."""
from dotenv import load_dotenv
load_dotenv()

from tinksync.tink import create_user, make_connect_bank_url, fetch_user_accounts, fetch_user_accounts, fetch_user_transactions
from tinksync.mongodb import get_user_settings, replace_user_settings, insert_user_settings

def _cli_create(username):
    if get_user_settings(username):
        print("User already exists!")
        return
    
    create_user(username)
    new_record = {
        "username" : username
    }
    insert_user_settings(new_record)
    print("User created.")


def _cli_get_accounts(username):
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

def _cli_set_account_nickname(username, account_id, nickname):
    user_settings = get_user_settings(username)
    if not user_settings:
        print("User does not exist!")
        return

    user_settings["accountNicknames"][account_id] = nickname
    replace_user_settings(user_settings)

def _cli_set_integration(username, integration_name, integration_settings):
    user_settings = get_user_settings(username)
    if not user_settings:
        print("User does not exist!")
        return

    user_settings['integrations'][integration_name] = integration_settings

def _cli_get_transactions(username):
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

def _main():
    import argparse, os, json

    # Exmaple usage:
    # tinksync --username <username> --create -> Will create a Tink user
    # tinksync --connect -> Will generate a bank connection URL
    # tinksync --accounts -> Will fetch the accounts for the user
    # tinksync --transactions -> Will fetch the transactions for the user
    # tinksync --nickname <account_id> <nickname> -> Will set the nickname for the account


    parser = argparse.ArgumentParser(description="Tinksync CLI")
    parser.add_argument("--username", type=str, help="The username to use", required=False)
    parser.add_argument("--create", action="store_true", help="Create a Tink user")
    parser.add_argument("--connect", action="store_true", help="Generate a bank connection URL")
    parser.add_argument("--accounts", action="store_true", help="Fetch the accounts for the user")
    parser.add_argument("--transactions", action="store_true", help="Fetch the transactions for the user")
    parser.add_argument("--nickname", nargs=2, help="Set the nickname for the account")

    args = parser.parse_args()

    username = args.username or os.environ.get("TINK_DEFAULT_USERNAME") or "myself"

    if args.create:
        _cli_create(username)
    elif args.connect:
        print(make_connect_bank_url(username))
    elif args.accounts:
        _cli_get_accounts(username)
    elif args.transactions:
        _cli_get_transactions(username)
    elif args.nickname:
        account_id = args.nickname[0]
        nickname = args.nickname[1]
        _cli_set_account_nickname(username, account_id, nickname)
