"""
Operations for interacting with Notion Pages.
"""
import logging
from typing import List, Dict, Optional
from .client import NotionClient

logger = logging.getLogger("notion_sync")

class PageOps:
    """
    Handles Page creation, updates, and retrieval in Notion.
    """
    def __init__(self, client: NotionClient):
        self.notion = client.get_client()

    def get_page(self, page_id: str) -> Optional[Dict]:
        """
        Retrieves a page by ID. Returns None if not found or inaccessible.
        """
        try:
            return self.notion.pages.retrieve(page_id=page_id)
        except Exception as e:  # pylint: disable=broad-except
            logger.warning("Could not retrieve page %s: %s", page_id, e)
            return None

    def get_all_blocks(self, block_id: str) -> List[Dict]:
        """
        Recursively retrieves all blocks for a page/block.
        """
        results = []
        has_more = True
        start_cursor = None
        
        while has_more:
            try:
                response = self.notion.blocks.children.list(
                    block_id=block_id, 
                    start_cursor=start_cursor
                )
                blocks = response['results']
                
                for block in blocks:
                    # Recurse if has children and is NOT a sub-page
                    if block.get('has_children', False) and block.get('type') != 'child_page':
                        block['children'] = self.get_all_blocks(block['id'])
                    results.append(block)
                    
                has_more = response['has_more']
                start_cursor = response['next_cursor']
            except Exception as e: # pylint: disable=broad-except
                logger.error("Failed to fetch blocks for %s: %s", block_id, e)
                return []
                
        return results

    def find_child_page(self, parent_id: str, title: str) -> Optional[str]:
        """
        Finds a child page with the given title inside parent_id.
        Iterates through children blocks looking for type='child_page'.
        """
        start_cursor = None
        has_more = True

        while has_more:
            try:
                response = self.notion.blocks.children.list(
                    block_id=parent_id,
                    start_cursor=start_cursor
                )
                for block in response['results']:
                    if block['type'] == 'child_page':
                        # child_page title is inside the child_page object
                        if block['child_page']['title'] == title:
                            return block['id']

                has_more = response['has_more']
                start_cursor = response['next_cursor']
            except Exception as e:  # pylint: disable=broad-except
                logger.error("Failed to list children of %s: %s", parent_id, e)
                return None
        return None

    def create_child_page(self, parent_id: str, title: str) -> str:
        """
        Creates an empty child page (Folder) inside parent_id.
        """
        return self.create_page(parent={"page_id": parent_id}, title=title, blocks=[])

    def create_page(
        self, parent: Dict, title: str, blocks: List[Dict], topic: Optional[str] = None
    ) -> str:
        """
        Creates a new page.
        parent: Dict, e.g. {"database_id": "..."} or {"page_id": "..."}
        """
        # Determine property name based on parent type
        title_key = "Name"  # Default for Database
        if "page_id" in parent:
            title_key = "title"  # For Child Page

        properties = {
            title_key: {
                "title": [
                    {
                        "text": {
                            "content": title
                        }
                    }
                ]
            }
        }

        # Only add topic if parent is Database (property exists there)
        if topic and "database_id" in parent:
            properties["Topic"] = {
                "select": {
                    "name": topic
                }
            }

        initial_blocks = blocks[:100]
        remaining_blocks = blocks[100:]

        try:
            response = self.notion.pages.create(
                parent=parent,
                properties=properties,
                children=initial_blocks
            )
        except Exception as e:  # pylint: disable=broad-except
            # Retry logic for Topic failure (only applicable if we tried setting it)
            if topic and "database_id" in parent and (
                "property" in str(e) or "validation" in str(e)
            ):
                logger.warning(
                    "Failed to create page with Topic '%s'. "
                    "Retrying without Topic property. (Error: %s)",
                    topic, e
                )
                del properties["Topic"]
                response = self.notion.pages.create(
                    parent=parent,
                    properties=properties,
                    children=initial_blocks
                )
            else:
                logger.error("Failed to create page: %s", e)
                raise e

        # Success handling
        page_id = response['id']
        logger.info("Created new page %s with %d blocks.", page_id, len(initial_blocks))

        try:
            if remaining_blocks:
                self.append_blocks(page_id, remaining_blocks)
        except Exception as append_error:  # pylint: disable=broad-except
            # Just log
            logger.error(
                "Page created %s, but failed to append remaining blocks: %s",
                page_id, append_error
            )
            raise append_error

        return page_id

    def update_page(self, page_id: str, blocks: List[Dict], topic: Optional[str] = None):
        """
        Updates an existing page: clears content and appends new blocks.
        Optionally updates the Topic property.
        """
        # 0. Update properties if needed
        if topic:
            try:
                self.notion.pages.update(
                    page_id=page_id,
                    properties={
                        "Topic": {
                            "select": {
                                "name": topic
                            }
                        }
                    }
                )
            except Exception as e:  # pylint: disable=broad-except
                logger.warning("Failed to update Topic property for %s: %s", page_id, e)

        # 1. Archive existing blocks
        self._clear_page_content(page_id)

        # 2. Append new blocks
        self.append_blocks(page_id, blocks)

    def append_blocks(self, page_id: str, blocks: List[Dict]):
        """
        Appends blocks to a page (block) in batches.
        """
        # Batching provided by logic
        batch_size = 100
        for i in range(0, len(blocks), batch_size):
            chunk = blocks[i:i + batch_size]
            try:
                self.notion.blocks.children.append(
                    block_id=page_id,
                    children=chunk
                )
                logger.debug("Appended batch of %d blocks to %s", len(chunk), page_id)
            except Exception as e:  # pylint: disable=broad-except
                logger.error("Failed to append blocks to %s: %s", page_id, e)
                raise e

    def _clear_page_content(self, page_id: str):
        """
        Archives all child blocks of a page.
        """
        has_more = True
        start_cursor = None

        while has_more:
            response = self.notion.blocks.children.list(block_id=page_id, start_cursor=start_cursor)
            blocks = response['results']
            has_more = response['has_more']
            start_cursor = response['next_cursor']

            for block in blocks:
                try:
                    self.notion.blocks.delete(block_id=block['id'])
                except Exception as e:  # pylint: disable=broad-except
                    logger.warning("Failed to delete block %s: %s", block['id'], e)

            logger.debug("Cleared batch of %d blocks from %s", len(blocks), page_id)

    def archive_page(self, page_id: str):
        """
        Archives (deletes) a page.
        """
        try:
            self.notion.pages.update(page_id=page_id, archived=True)
            logger.info("Archived page %s", page_id)
        except Exception as e:  # pylint: disable=broad-except
            logger.error("Failed to archive page %s: %s", page_id, e)
            raise e
