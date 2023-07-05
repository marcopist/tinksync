#!usr/bin/env python

"""This module contains a CLI which can be used to create a Tink user, generate a bank connection URL, and fetch the accounts."""
from dotenv import load_dotenv

load_dotenv()

from tinksync.tink import create_user, make_connect_bank_url, fetch_user_accounts, fetch_user_accounts, fetch_user_transactions
from pprint import pprint


def _format_accounts(data):
    accounts = data["accounts"]
    for account in accounts:
        name = account["name"]
        balance_val = account["balances"]["booked"]["amount"]["value"]
        balance = float(balance_val["unscaledValue"]) / 10 ** int(balance_val["scale"])
        currency = account["balances"]["booked"]["amount"]["currencyCode"]
        account_id = account["id"]
        print(f">> {account_id} > {name} > {balance} {currency} > OK")


def _format_transactions(data):
    transactions = data["transactions"]
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
    # python -m tinksync.cli --username <username> --create -> Will create a Tink user
    # python -m tinksync.cli --connect -> Will generate a bank connection URL
    # python -m tinksync.cli --accounts -> Will fetch the accounts for the user
    # python -m tinksync.cli --transactions -> Will fetch the transactions for the user

    parser = argparse.ArgumentParser(description="Tinksync CLI")
    parser.add_argument("--username", type=str, help="The username to use", required=False)
    parser.add_argument("--create", action="store_true", help="Create a Tink user")
    parser.add_argument("--connect", action="store_true", help="Generate a bank connection URL")
    parser.add_argument("--accounts", action="store_true", help="Fetch the accounts for the user")
    parser.add_argument("--transactions", action="store_true", help="Fetch the transactions for the user")

    args = parser.parse_args()

    username = args.username or os.environ.get("TINK_USERNAME") or "myself"
    debug_mode = True if os.environ.get("DEBUG_MODE") == 1 else False

    if args.create:
        print(create_user(username, debug=debug_mode))
    elif args.connect:
        print(make_connect_bank_url(username, debug=debug_mode))
    elif args.accounts:
        _format_accounts(fetch_user_accounts(username, debug=debug_mode))
    elif args.transactions:

        print(json.dumps((fetch_user_transactions(username, debug=debug_mode)), indent=4))
