import os
import logging
import frontmatter
from pathlib import Path
from typing import Dict, Optional, Set, List
from notion_sync.notion.page_ops import PageOps
from notion_sync.parser.block_to_markdown import BlockToMarkdown

logger = logging.getLogger("notion_sync")

class PullManager:
    def __init__(self, page_ops: PageOps, source_dir: Path):
        self.page_ops = page_ops
        self.source_dir = source_dir
        self.converter = BlockToMarkdown()
        self.id_map: Dict[str, Path] = {}
        self._build_id_map()

    def _build_id_map(self):
        """
        Scans local files to map Notion IDs to file paths.
        """
        for file_path in self.source_dir.glob("**/*.md"):
            try:
                post = frontmatter.load(str(file_path))
                pid = post.metadata.get('notion_page_id')
                if pid:
                    # Normalize ID just in case
                    pid = pid.replace('-', '')
                    self.id_map[pid] = file_path
            except Exception as e:
                logger.warning("Failed to read frontmatter from %s: %s", file_path, e)

    def pull_sync(self, root_page_id: str):
        """
        Starts the pull sync from the root page.
        """
        logger.info("Starting Pull Sync from Root %s...", root_page_id)
        # Root page content -> source_dir / index.md (usually)
        # But we act recursively.
        self._process_page(root_page_id, self.source_dir, is_root=True)

    def _process_page(self, page_id: str, current_dir: Path, is_root: bool = False):
        """
        Fetches page content, decides path, writes file, and recurses children.
        """
        # 1. Fetch Page Info
        page = self.page_ops.get_page(page_id)
        if not page:
            logger.error("Could not fetch page %s", page_id)
            return

        title = self._get_page_title(page)
        
        # 2. Fetch Blocks (Content + Children)
        blocks = self.page_ops.get_all_blocks(page_id)
        
        # 3. separate content blocks from child_page blocks
        content_blocks = []
        child_pages = []
        for b in blocks:
            if b['type'] == 'child_page':
                child_pages.append(b)
            else:
                content_blocks.append(b)
                
        # 4. Determine File Path
        if is_root:
            target_path = current_dir / "index.md"
        else:
            # Check existing map
            clean_id = page_id.replace('-', '')
            if clean_id in self.id_map:
                target_path = self.id_map[clean_id]
                # If we have children, ensure target_path is index.md or move it?
                if child_pages and target_path.name != "index.md":
                    # Needs promotion to folder
                    logger.info("Promoting %s to folder structure...", target_path)
                    new_folder = target_path.with_suffix('') # remove .md
                    new_folder.mkdir(exist_ok=True)
                    new_path = new_folder / "index.md"
                    target_path.rename(new_path)
                    target_path = new_path
                    self.id_map[clean_id] = target_path
            else:
                # New file
                safe_title = self._sanitize_filename(title)
                if child_pages:
                    # Create folder
                    folder_path = current_dir / safe_title
                    folder_path.mkdir(exist_ok=True)
                    target_path = folder_path / "index.md"
                else:
                    target_path = current_dir / f"{safe_title}.md"
        
        # 5. Write Content
        self._write_file(target_path, page_id, title, content_blocks)
        
        # 6. Recurse Children
        for child in child_pages:
            child_id = child['id']
            # Sub-folder is the parent directory of the current file if it's index.md
            # If target_path is `foo/index.md`, children go in `foo/`
            # If target_path is `foo.md`, children go in... wait.
            # We guaranteed if child_pages exist, type is Folder (index.md).
            
            # Determine base dir for children
            if target_path.name == "index.md":
                child_base = target_path.parent
            else:
                # Should not happen given logic above, but fallback
                child_base = target_path.parent / target_path.stem
                child_base.mkdir(exist_ok=True)
                
            self._process_page(child_id, child_base)

    def _write_file(self, path: Path, page_id: str, title: str, blocks: List[Dict]):
        """
        Converts blocks to MD and writes to file with frontmatter.
        """
        md_content = self.converter.convert(blocks)
        
        # Prepare Frontmatter
        metadata = {
            "notion_page_id": page_id,
            "title": title
        }
        
        # If file exists, preserve other metadata?
        if path.exists():
            try:
                post = frontmatter.load(str(path))
                post.content = md_content
                # Update essential fields only
                post.metadata['notion_page_id'] = page_id
                # post.metadata['title'] = title # Optional: update title sync?
                
                with open(path, 'w', encoding='utf-8') as f:
                    f.write(frontmatter.dumps(post))
                    
                logger.info("Updated local file %s", path)
                return
            except Exception:
                logger.warning("Could not read existing file %s. Overwriting.", path)
        
        # Create new
        post = frontmatter.Post(md_content, **metadata)
        
        # Ensure parent exists
        path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(path, 'w', encoding='utf-8') as f:
            f.write(frontmatter.dumps(post))
        logger.info("Created local file %s", path)

    def _get_page_title(self, page: Dict) -> str:
        props = page.get('properties', {})
        # Try 'title' (Page) or 'Name' (DB)
        title_obj = []
        if 'title' in props:
            title_obj = props['title']['title']
        elif 'Name' in props:
             title_obj = props['Name']['title']
             
        if title_obj:
            return title_obj[0].get('plain_text', 'Untitled')
        return "Untitled"

    def _sanitize_filename(self, name: str) -> str:
        # Simple sanitization
        keepcharacters = (' ','.','_','-')
        return "".join(c for c in name if c.isalnum() or c in keepcharacters).strip().replace(' ', '_')
