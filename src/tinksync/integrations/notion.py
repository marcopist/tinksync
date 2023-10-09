import os, requests
from tinksync._utils import _debug
from tinksync.integrations.base import Integration


class NotionIntegration(Integration):
    def _set_credentials(self, config):
        self._NOTION_SECRET = config.get("notionSecret")
        self._NOTION_DATABASE_ID = config.get("notionDatabaseId")

        return self._NOTION_SECRET and self._NOTION_DATABASE_ID

    def _get_target_transactions(self):
        url = f"https://api.notion.com/v1/databases/{self._NOTION_DATABASE_ID}/query"
        headers = {
            "Authorization": f"Bearer {self._NOTION_SECRET}",
            "Notion-Version": "2022-06-28",
        }
        res = requests.post(url, headers=headers)
        _debug(res)
        results = res.json()["results"]
        return {result["properties"]["Name"]["title"][0]["text"]["content"]: result["properties"] for result in results}
    
    def _publish_transactions(self, transactions):
        pass


if __name__ == "__main__":
    from tinksync.mongodb import get_user_settings
    settings = get_user_settings("marcopist")
    config = settings['integrations'][1]['NotionIntegration']
    print(f"{config=}")
    notion = NotionIntegration("marcopist", config)  # type: ignore
    print(notion._get_target_transactions())
    