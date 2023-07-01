from abc import ABC, abstractmethod
from tinksync.tink import fetch_user_transactions

class Integration:
    def __init__(self, username):
        self.username = username

    def get_credentials(self):
        pass

    def get_transactions(self):
        return fetch_user_transactions(self.username)
    
    def reconciliate(self):
        pass