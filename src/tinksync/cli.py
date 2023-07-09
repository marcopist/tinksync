#!usr/bin/env python

"""This module contains a CLI which can be used to create a Tink user, generate a bank connection URL, and fetch the accounts."""
from dotenv import load_dotenv
load_dotenv()



def _main():
    """This function is the entrypoint of the CLI."""
    import argparse, os, json
    from tinksync.main import cli_create, cli_get_accounts, cli_get_transactions, cli_set_account_nickname
    from tinksync.tink import make_connect_bank_url

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
        cli_create(username)
    elif args.connect:
        print(make_connect_bank_url(username))
    elif args.accounts:
        cli_get_accounts(username)
    elif args.transactions:
        cli_get_transactions(username)
    elif args.nickname:
        account_id = args.nickname[0]
        nickname = args.nickname[1]
        cli_set_account_nickname(username, account_id, nickname)
