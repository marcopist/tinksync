import os, requests
from tinksync._utils import _debug

from tinksync.integrations.base import Integration
from pprint import pprint

class CodaIntegration(Integration):
    def _get_credentials(self):
        CODA_DOC_ID = os.environ.get("CODA_DOC_ID")
        CODA_API_KEY = os.environ.get("CODA_API_KEY")
        CODA_TABLE_ID = os.environ.get("CODA_TABLE_ID")

        if not (CODA_DOC_ID and CODA_API_KEY and CODA_TABLE_ID):
            # Credentials not found
            # This integration is not applicable
            # TODO: Log this
            print("Coda credentials not found")
            return None

        # Credentials found
        # This integration is applicable
        # TODO: Log this
        return dict(CODA_DOC_ID=CODA_DOC_ID, CODA_API_KEY=CODA_API_KEY, CODA_TABLE_ID=CODA_TABLE_ID)

    def _get_target_transactions(self):
        headers = {"Authorization": f'Bearer {self.credentials["CODA_API_KEY"]}'}  # type: ignore
        docid = self.credentials["CODA_DOC_ID"]  # type: ignore
        tableid = self.credentials["CODA_TABLE_ID"]  # type: ignore
        colums_url = f"https://coda.io/apis/v1/docs/{docid}/tables/{tableid}/columns"
        colums_res = requests.get(colums_url, headers=headers)

        rows_url = f"https://coda.io/apis/v1/docs/{docid}/tables/{tableid}/rows"
        rows_res = requests.get(rows_url, headers=headers)
        cols_mapping = {col['id'] : col['name'] for col in colums_res.json()["items"]}

        transactions = {
            row["name"] : {
                cols_mapping[prop]: row["values"][prop]
                for prop in row["values"]
            }
            for row in rows_res.json()["items"]
            if row["name"] != ""
        }
        return transactions
    
    def _publish_transactions(self, transactions):
        headers = {"Authorization": f'Bearer {self.credentials["CODA_API_KEY"]}'}  # type: ignore
        docid = self.credentials["CODA_DOC_ID"]  # type: ignore
        tableid = self.credentials["CODA_TABLE_ID"]  # type: ignore
        colums_url = f"https://coda.io/apis/v1/docs/{docid}/tables/{tableid}/columns"
        colums_res = requests.get(colums_url, headers=headers)
        cols_mapping = {col['name'] : col['id'] for col in colums_res.json()["items"]}

        mapped_transactions = {
            'rows': [
                {
                    'cells': [
                        {
                            'column': cols_mapping[k],
                            'value': v
                        }
                        for k, v in single_transaction.items()
                    ]
                }
            ] for single_transaction in transactions.values()
        }

        print(mapped_transactions)







if __name__ == "__main__":
    coda = CodaIntegration("test")
    current = coda._get_target_transactions()
    pprint(coda._publish_transactions(current))
