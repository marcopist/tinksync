from abc import ABC, abstractmethod
from tinksync.tink import fetch_user_transactions
from tinksync.mongodb import get_user_settings

class Integration(ABC):
    def __init__(self, username, config):
        self.username = username
        self.is_applicable = self._set_credentials(config)

    @abstractmethod
    def _set_credentials(self, config):
        pass

    @abstractmethod
    def _get_target_transactions(self):
        """This function returns a list of dictionaries.
        The key of the dict is the Tink transaction ID.
        The value is the transaction itself."""
        pass

    @abstractmethod
    def _publish_transactions(self, transactions):
        pass

    def _format_source_transactions(self, source_transactions):
        return {
            transaction["id"]: {
                "Amount": float(transaction["amount"]["value"]["unscaledValue"]) / 10 ** float(transaction["amount"]["value"]["scale"]),
                "Merchant": transaction["descriptions"]["display"],
                "Date": transaction["dates"]["booked"],
                "Key": transaction["id"],
                "Account": get_user_settings(self.username)["accountNicknames"][transaction["accountId"]], # type: ignore
            }
            for transaction in source_transactions["transactions"]
        }

    def reconciliate(self, source_transactions_raw):
        target_transactions = self._get_target_transactions()
        source_transactions = self._format_source_transactions(source_transactions_raw)
        missing_transaction_keys = set(source_transactions.keys()) - set(target_transactions.keys())  # type: ignore
        missing_transactions = {key: source_transactions[key] for key in missing_transaction_keys}
        self._publish_transactions(missing_transactions)
