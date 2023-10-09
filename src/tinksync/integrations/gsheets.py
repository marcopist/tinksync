import gspread, json
from tinksync.integrations.base import Integration


class GSheetsIntegration(Integration):
    def _set_credentials(self, config):
        SPREADSHEET_KEY = config.get("gSheetsKey")
        SPREADSHEET_TAB = config.get("gSheetsTab")
        GSHEETS_CREDENTIALS_RAW = config.get("gSheetsCredentials")
        GSHEETS_CREDENTIALS = json.loads(GSHEETS_CREDENTIALS_RAW)
        self.gc = gspread.service_account_from_dict(GSHEETS_CREDENTIALS)
        self.sh = self.gc.open_by_key(SPREADSHEET_KEY)
        self.tab = self.sh.worksheet(SPREADSHEET_TAB)
        return True

    def _get_target_transactions(self):
        records_raw = self.tab.get_all_records()
        records = {record_raw["Key"]: record_raw for record_raw in records_raw}
        return records
    
    def _publish_transactions(self, transactions):
        rows = [(
            transaction["Key"],
            transaction["Amount"],
            transaction["Merchant"],
            transaction["Date"],
            transaction["Account"],
        ) for key, transaction in transactions.items()]
        
        self.tab.append_rows(rows)
    

if __name__ == "__main__":
    from tinksync.mongodb import get_user_settings

    username = "marcopist"

    user_settings = get_user_settings(username)
    integration_settings = user_settings["integrations"]
    for integration_config in integration_settings:
        integration_type = list(integration_config.keys())[0]
        if integration_type != "GSheetsIntegration":
            continue
        
        integration_credentials = integration_config[integration_type]
        integration_class = GSheetsIntegration
        integration_instance = integration_class(username, integration_credentials)
        integration_instance.reconciliate()


