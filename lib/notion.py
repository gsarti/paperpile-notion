from typing import Dict

from notion_database.database import Database
from notion_database.page import Page

from .notion_utils import parse_db_content, Properties


class NotionDBInterface:
    def __init__(self, database_id: str, integration_token: str):
        self.database_id = database_id
        self.integration_token = integration_token
        self.db = Database(integration_token)
        self.pages = None

    def query_database(self):
        self.db.find_all_page(self.database_id) 
        self.pages = parse_db_content(self.db.result['results'])
    
    def create_page(self, entry: Dict[str, Dict[str, str]]):
        page = Page(self.integration_token)
        properties = Properties.from_entry(entry)
        page.create_page(self.database_id, properties)

    def update_page(self, page_id: str, entry: Dict[str, Dict[str, str]]):
        page = Page(self.integration_token)
        page.update_page(page_id, Properties.from_entry(entry))
    