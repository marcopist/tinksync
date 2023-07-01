"""This module contains a CLI which can be used to create a Tink user, generate a bank connection URL, and fetch the accounts."""

if __name__ == "__main__":
    from dotenv import load_dotenv
    import argparse, os
    # Exmaple usage:
    # python -m tinksync.cli --username <username> --create -> Will create a Tink user
    # python -m tinksync.cli --connect -> Will generate a bank connection URL
    # python -m tinksync.cli --accounts -> Will fetch the accounts for the user
    # python -m tinksync.cli --transactions -> Will fetch the transactions for the user

    load_dotenv()

    from tinksync.tink import create_user, make_connect_bank_url, fetch_user_accounts, fetch_user_accounts, fetch_user_transactions

    parser = argparse.ArgumentParser(description="Tinksync CLI")
    parser.add_argument("--username", type=str, help="The username to use", required=False)
    parser.add_argument("--create", action="store_true", help="Create a Tink user")
    parser.add_argument("--connect", action="store_true", help="Generate a bank connection URL")
    parser.add_argument("--accounts", action="store_true", help="Fetch the accounts for the user")
    parser.add_argument("--transactions", action="store_true", help="Fetch the transactions for the user")

    args = parser.parse_args()

    username = args.username or os.environ.get("TINK_USERNAME") or "myself"
    debug_mode = True if os.environ.get("DEBUG_MODE") else False

    if args.create:
        print(create_user(username, debug=debug_mode))
    elif args.connect:
        print(make_connect_bank_url(username, debug=debug_mode))
    elif args.accounts:
        print(fetch_user_accounts(username, debug=debug_mode))
    elif args.transactions:
        print(fetch_user_transactions(username, debug=debug_mode))