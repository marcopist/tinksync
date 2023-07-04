from abc import ABC, abstractmethod
from tinksync.tink import fetch_user_transactions


class Integration(ABC):
    def __init__(self, username):
        self.username = username
        self.credentials = self._get_credentials()

    def is_applicable(self):
        return self.credentials is not None

    @abstractmethod
    def _get_credentials(self):
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

    def reconciliate(self, source_transactions):
        target_transactions = self._get_target_transactions()
        missing_transaction_keys = set(source_transactions.keys()) - set(target_transactions.keys())  # type: ignore
        missing_transactions = {key : source_transactions[key] for key in missing_transaction_keys}

