import os
import sys
import argparse
import frontmatter
from typing import List, Optional
from pathlib import Path

# Add project root to path to allow imports
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)
sys.path.append(project_root)

from notion_sync.utils.logging import setup_logging, get_logger
from notion_sync.parser.markdown_parser import MarkdownParser
from notion_sync.validation.markdown_validator import MarkdownValidator
from notion_sync.validation.block_validator import BlockValidator
from notion_sync.validation.frontmatter_validator import FrontmatterValidator
from notion_sync.notion.client import NotionClient
from notion_sync.notion.page_ops import PageOps

logger = get_logger()

class SyncManager:
    def __init__(self, token: Optional[str], root_page_id: Optional[str], source_dir: Path, dry_run: bool):
        self.dry_run = dry_run
        self.root_page_id = root_page_id
        self.source_dir = source_dir
        self.topic_page_cache = {}
        
        # Initialize modules
        self.md_parser = MarkdownParser()
        self.md_validator = MarkdownValidator()
        self.block_validator = BlockValidator()
        self.fm_validator = FrontmatterValidator()
        
        if not dry_run:
            client = NotionClient(token)
            self.page_ops = PageOps(client)
        else:
            self.page_ops = None

    def sync_file(self, file_path: Path) -> Optional[str]:
        """
        Syncs a single file. Returns notion_page_id if successful, None otherwise.
        """
        logger.info(f"Processing {file_path}...")
        
        try:
            # 1. Read Content
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            # 2. Validation
            # A. Markdown Validation
            md_errors = self.md_validator.validate(content)
            if md_errors:
                logger.error(f"Markdown validation failed for {file_path}:")
                for err in md_errors:
                    logger.error(f"  - {err}")
                return None
                
            # Parse and get blocks
            metadata, blocks = self.md_parser.parse_file(str(file_path))
            
            # B. Frontmatter Validation
            fm_errors = self.fm_validator.validate(metadata)
            if fm_errors:
                logger.error(f"Frontmatter validation failed for {file_path}:")
                for err in fm_errors:
                    logger.error(f"  - {err}")
                return None

            # C. Block Validation
            block_errors = self.block_validator.validate_blocks(blocks)
            if block_errors:
                logger.error(f"Block validation failed for {file_path}:")
                for err in block_errors:
                    logger.error(f"  - {err}")
                return None

            # 3. Sync Logic
            page_id = metadata.get('notion_page_id')
            title = file_path.stem # Default title is filename
            
            # Determine Hierarchy
            rel_path = file_path.relative_to(self.source_dir)
            
            # Recursive Folder Resolution
            current_parent_id = self.root_page_id
            
            # Iterate over all folder parts (excluding the filename)
            # e.g. docs/Kubernetes/commands/file.md -> ('Kubernetes', 'commands')
            for folder_name in rel_path.parts[:-1]:
                current_parent_id = self._get_or_create_folder(current_parent_id, folder_name)
                if not current_parent_id:
                     logger.error(f"Failed to resolve folder structure for {file_path}")
                     return None

            parent_ref = {"page_id": current_parent_id}
            
            # Sub-pages don't need 'Topic' property
            topic = None 

            if self.dry_run:
                logger.info(f"[DRY RUN] Would {'update' if page_id else 'create'} page for {file_path}")
                logger.info(f"[DRY RUN] Parent: {parent_ref}")
                logger.info(f"[DRY RUN] Blocks generated: {len(blocks)}")
                return page_id if page_id else f"dry-run-new-{file_path}"
                
            if page_id:
                # Update existing page
                logger.info(f"Updating page {page_id}")
                try:
                    # Update content. Topic arg is not used for pages, pass None.
                    self.page_ops.update_page(page_id, blocks, topic=None)
                    return page_id
                except Exception as e:
                    # If page not found, recreate it
                    if "Could not find" in str(e) or "404" in str(e) or "validation" in str(e): 
                        logger.warning(f"Page {page_id} not found or inaccessible. Re-creating. (Error: {e})")
                        page_id = None
                    else:
                        logger.error(f"Failed to update page {page_id}: {e}")
                        return None

            if not page_id:
                # Create new page
                if not self.root_page_id:
                    logger.error(f"Cannot create new page for {file_path}: No root_page_id provided.")
                    return None
                    
                logger.info(f"Creating new page (Parent: {parent_ref})")
                new_page_id = self.page_ops.create_page(parent_ref, title, blocks, topic=None)
                
                # Write back page_id
                self._update_frontmatter(file_path, new_page_id)
                return new_page_id
            
        except Exception as e:
            logger.error(f"Failed to sync {file_path}: {e}")
            return None

    def _get_or_create_folder(self, parent_id: str, folder_name: str) -> Optional[str]:
        """
        Gets or creates a folder page with title 'folder_name' inside 'parent_id'.
        """
        if self.dry_run:
            return f"dry-run-folder-{folder_name}"
            
        cache_key = f"{parent_id}:{folder_name}"
        if cache_key in self.topic_page_cache:
            return self.topic_page_cache[cache_key]
            
        # Find existing
        folder_id = self.page_ops.find_child_page(parent_id, folder_name)
        if not folder_id:
            logger.info(f"Creating Folder Page '{folder_name}' inside {parent_id}...")
            # create_child_page uses create_page which uses existing logic
            folder_id = self.page_ops.create_child_page(parent_id, folder_name)
            
        if folder_id:
            self.topic_page_cache[cache_key] = folder_id
            
        return folder_id

    def _update_frontmatter(self, file_path: Path, page_id: str):
        """
        Updates the local markdown file with the new notion_page_id.
        """
        post = frontmatter.load(str(file_path))
        post.metadata['notion_page_id'] = page_id
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(frontmatter.dumps(post))
        
        logger.info(f"Updated local file {file_path} with notion_page_id: {page_id}")

import argparse
from dotenv import load_dotenv

def main():
    # Load .env file
    load_dotenv()
    
    parser = argparse.ArgumentParser(description="Sync Markdown files to Notion.")
    parser.add_argument("directory", help="Directory containing markdown files.")
    parser.add_argument("--dry-run", action="store_true", help="Perform a dry run without writing to Notion.")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose logging.")
    parser.add_argument("--root-page-id", help="Notion Root Page ID. Defaults to NOTION_ROOT_PAGE_ID env var.")
    parser.add_argument("--pull", action="store_true", help="Sync FROM Notion TO Local (Pull).")
    
    args = parser.parse_args()
    
    setup_logging(args.verbose)
    
    root_id = args.root_page_id or os.environ.get("NOTION_ROOT_PAGE_ID")
    token = os.environ.get("NOTION_TOKEN")
    
    if not args.dry_run and not token:
        logger.error("NOTION_TOKEN environment variable is required.")
        sys.exit(1)
        
    source_dir = Path(args.directory)
    if not source_dir.exists():
        logger.error(f"Directory not found: {source_dir}")
        sys.exit(1)

    try:
        manager = SyncManager(token, root_id, source_dir, args.dry_run)
    except Exception as e:
        logger.error(f"Initialization failed: {e}")
        sys.exit(1)
        
    # PULL Mode
    if args.pull:
        if not root_id:
             logger.error("Root Page ID is required for Pull Sync.")
             sys.exit(1)
        if args.dry_run:
             logger.warning("Dry-run not fully implemented for Pull. Operations will write to disk.")

        from notion_sync.pull import PullManager
        try:
            puller = PullManager(manager.page_ops, source_dir)
            puller.pull_sync(root_id)
            logger.info("Pull Sync Complete.")
            sys.exit(0)
        except Exception as e:
            logger.error(f"Pull Sync failed: {e}")
            sys.exit(1)
        
    files = list(source_dir.glob("**/*.md"))
    if not files:
        logger.warning(f"No markdown files found in {source_dir}")
        sys.exit(0)
        
    stats = {
        "processed": 0,
        "synced": 0,
        "failed": 0
    }
    
    # Track seen page IDs to detect orphans and duplicates
    seen_page_ids = set()
    
    for file_path in files:
        stats["processed"] += 1
        page_id = manager.sync_file(file_path) # sync_file needs to return page_id if successful
        if page_id:
            if page_id in seen_page_ids:
                logger.error(f"Duplicate Notion Page ID {page_id} found in {file_path}. Skipping.")
                stats["failed"] += 1
                continue
            seen_page_ids.add(page_id)
            stats["synced"] += 1
        else:
            stats["failed"] += 1

    # Cleanup Orphans (Deleted Files) - DISABLED for Page Mode
    # Implementing orphan cleanup in a tree structure requires traversing the tree.
    # For now, we disable it to ensure safety and stability in the pivot.
    # if not args.dry_run and root_id:
    #     logger.info("Orphan cleanup is currently disabled in Page Tree mode.")

    logger.info("Sync Complete.")
    logger.info(f"Processed: {stats['processed']}")
    logger.info(f"Synced:    {stats['synced']}")
    logger.info(f"Failed:    {stats['failed']}")
    
    if stats["failed"] > 0:
        sys.exit(1)

if __name__ == "__main__":
    main()
