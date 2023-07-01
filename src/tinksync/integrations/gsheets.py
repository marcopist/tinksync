import os
from tinksync.integrations.base import Integration

class GSheetsIntegration(Integration):
    def __init__(self, username):
        super().__init__(username)
        self.credentials = self.get_credentials()

    def get_credentials(self):
        self.