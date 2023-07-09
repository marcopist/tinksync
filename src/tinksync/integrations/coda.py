import os, requests
from tinksync._utils import _debug
from tinksync.integrations.base import Integration
#from tinksync.mongodb import get_user_settings, replace_user_settings, insert_user_settings


class CodaIntegration(Integration):
    def _set_credentials(self, config):
        self._CODA_DOC_ID = config.get("codaDocId")
        self._CODA_API_KEY = config.get("codaApiKey")
        self._CODA_TABLE_ID = config.get("codaTableId")

        return self._CODA_DOC_ID and self._CODA_API_KEY and self._CODA_TABLE_ID

    def _get_target_transactions(self):
        headers = {"Authorization": f"Bearer {self._CODA_API_KEY}"}  # type: ignore # type: ignore
        colums_url = f"https://coda.io/apis/v1/docs/{self._CODA_DOC_ID}/tables/{self._CODA_TABLE_ID}/columns"

        colums_res = requests.get(colums_url, headers=headers)
        _debug(colums_res)

        rows_url = f"https://coda.io/apis/v1/docs/{self._CODA_DOC_ID}/tables/{self._CODA_TABLE_ID}/rows"

        rows_res = requests.get(rows_url, headers=headers)
        _debug(colums_res)

        cols_mapping = {col["id"]: col["name"] for col in colums_res.json()["items"]}

        transactions = {
            row["name"]: {cols_mapping[prop]: row["values"][prop] for prop in row["values"]}
            for row in rows_res.json()["items"]
            if row["name"] != ""
        }
        return transactions

    def _publish_transactions(self, transactions):
        headers = {"Authorization": f"Bearer {self._CODA_API_KEY}"}
        colums_url = f"https://coda.io/apis/v1/docs/{self._CODA_DOC_ID}/tables/{self._CODA_TABLE_ID}/columns"

        colums_res = requests.get(colums_url, headers=headers)
        _debug(colums_res)

        cols_mapping = {col["name"]: col["id"] for col in colums_res.json()["items"]}
        payload = {
            "rows": [
                {"cells": [{"column": cols_mapping[k], "value": v} for k, v in single_transaction.items()]}
                for single_transaction in transactions.values()
            ]
        }

        rows_url = f"https://coda.io/apis/v1/docs/{self._CODA_DOC_ID}/tables/{self._CODA_TABLE_ID}/rows"
        publish_res = requests.post(rows_url, headers=headers, json=payload)
        _debug(publish_res)
