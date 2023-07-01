"""This module contains a CLI which can be used to create a Tink user, generate a bank connection URL, and fetch the accounts."""

from tinksync.tink import create_user, make_connect_bank_url, fetch_user_accounts, fetch_user_accounts, fetch_user_transactions


if __name__ == "__main__":
    import argparse
    # Exmaple usage:
    # python -m tinksync.cli --username <username> --create -> Will create a Tink user
    # python -m tinksync.cli --username <username> --connect -> Will generate a bank connection URL
    # python -m tinksync.cli --username <username> --accounts -> Will fetch the accounts for the user
    # python -m tinksync.cli --username <username> --transactions -> Will fetch the transactions for the user

    parser = argparse.ArgumentParser(description="Tink CLI")
    parser.add_argument("--username", type=str, help="The username to use")
    parser.add_argument("--create", action="store_true", help="Create a Tink user")
    parser.add_argument("--connect", action="store_true", help="Generate a bank connection URL")
    parser.add_argument("--accounts", action="store_true", help="Fetch the accounts for the user")
    parser.add_argument("--transactions", action="store_true", help="Fetch the transactions for the user")

    args = parser.parse_args()

    if args.create:
        print(create_user(args.username))
    elif args.connect:
        print(make_connect_bank_url(args.username))
    elif args.accounts:
        print(fetch_user_accounts(args.username))
    elif args.transactions:
        print(fetch_user_transactions(args.username))