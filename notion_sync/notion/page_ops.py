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
        # 0. Ensure parent chain is active (check for archived ancestors)
        try:
            self.ensure_parent_chain_active(page_id)
        except Exception as e:  # pylint: disable=broad-except
            logger.warning("Could not verify parent chain for %s: %s", page_id, e)

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
        Automatically handles archived ancestor errors by restoring parent chain.
        """
        # Ensure page itself and parent chain are active before appending
        try:
            self.ensure_parent_chain_active(page_id)
        except Exception as e:  # pylint: disable=broad-except
            logger.warning("Could not verify parent chain for %s before appending: %s", page_id, e)

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
                error_msg = str(e).lower()
                # Check if error is due to archived ancestor
                if "archived" in error_msg and ("ancestor" in error_msg or "parent" in error_msg):
                    logger.warning(
                        "Detected archived ancestor error for page %s. Attempting to restore parent chain...",
                        page_id
                    )
                    try:
                        # Try to restore parent chain
                        if self.ensure_parent_chain_active(page_id):
                            # Retry the append after restoring parents
                            logger.info("Retrying block append after restoring parent chain...")
                            self.notion.blocks.children.append(
                                block_id=page_id,
                                children=chunk
                            )
                            logger.debug("Successfully appended batch of %d blocks to %s after restoring parents", len(chunk), page_id)
                        else:
                            logger.error("Failed to restore parent chain for %s", page_id)
                            raise e
                    except Exception as retry_error:  # pylint: disable=broad-except
                        logger.error(
                            "Failed to restore parent chain and retry append for %s: %s",
                            page_id, retry_error
                        )
                        raise e
                else:
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

    def is_page_archived(self, page_id: str) -> bool:
        """
        Checks if a page is archived.
        """
        try:
            page = self.get_page(page_id)
            if page:
                return page.get('archived', False)
            return False
        except Exception as e:  # pylint: disable=broad-except
            logger.warning("Could not check archived status for page %s: %s", page_id, e)
            return False

    def unarchive_page(self, page_id: str):
        """
        Unarchives (restores) a page.
        """
        try:
            self.notion.pages.update(page_id=page_id, archived=False)
            logger.info("Unarchived page %s", page_id)
        except Exception as e:  # pylint: disable=broad-except
            logger.error("Failed to unarchive page %s: %s", page_id, e)
            raise e

    def ensure_parent_chain_active(self, page_id: str) -> bool:
        """
        Ensures all parent pages in the chain are not archived.
        First collects all ancestors from root to child, then unarchives from root down.
        Returns True if all parents are active, False otherwise.
        """
        try:
            # Step 1: Collect the entire chain from root to target page
            chain = self._collect_parent_chain(page_id)
            if not chain:
                logger.error("Could not collect parent chain for page %s", page_id)
                return False

            # Step 2: Unarchive from root to child (top-down)
            # This is critical: we must unarchive parents before children
            for ancestor_id in chain:
                if self.is_page_archived(ancestor_id):
                    logger.warning("Unarchiving page %s (parent chain restoration)", ancestor_id)
                    try:
                        self.unarchive_page(ancestor_id)
                    except Exception as e:  # pylint: disable=broad-except
                        # If unarchiving fails, it's likely because a parent is still archived
                        # Log and continue - we'll try again from the root
                        logger.warning(
                            "Failed to unarchive %s, may need to unarchive parent first: %s",
                            ancestor_id, e
                        )
                        # If this is the root, the error is real
                        if ancestor_id == chain[0]:
                            logger.error("Failed to unarchive root ancestor %s: %s", ancestor_id, e)
                            return False

            return True
        except Exception as e:  # pylint: disable=broad-except
            logger.error("Failed to ensure parent chain is active for %s: %s", page_id, e)
            return False

    def _collect_parent_chain(self, page_id: str) -> List[str]:
        """
        Collects the parent chain from root to target page.
        Returns a list of page IDs starting from root ancestor to target page.
        """
        chain = []
        current_id = page_id
        
        while current_id:
            page = self.get_page(current_id)
            if not page:
                break
            
            # Add current page to chain (we'll unarchive from root to child)
            chain.insert(0, current_id)  # Insert at beginning to maintain root-to-child order
            
            # Get parent
            parent = page.get('parent')
            if not parent:
                break
                
            # Check parent type
            if parent.get('type') == 'page_id':
                current_id = parent.get('page_id')
            elif parent.get('type') == 'workspace':
                # Root level reached
                break
            elif parent.get('type') == 'database_id':
                # Parent is a database, stop here
                break
            else:
                break
        
        return chain
