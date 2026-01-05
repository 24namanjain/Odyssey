import os
from notion_client import Client
from typing import Optional

class NotionClient:
    def __init__(self, token: Optional[str] = None):
        if not token:
            token = os.environ.get("NOTION_TOKEN")
        if not token:
            raise ValueError("NOTION_TOKEN environment variable is not set.")
            
        self.client = Client(auth=token)

    def get_client(self) -> Client:
        return self.client
