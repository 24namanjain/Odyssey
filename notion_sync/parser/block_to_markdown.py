import logging
from typing import List, Dict, Any

logger = logging.getLogger("notion_sync")

class BlockToMarkdown:
    """
    Converts Notion Blocks to Markdown text.
    """
    def __init__(self):
        self.list_depth = 0
        self.number_index_stack = []

    def convert(self, blocks: List[Dict]) -> str:
        """
        Converts a list of blocks to a markdown string.
        """
        lines = []
        for block in blocks:
            text = self._convert_block(block)
            if text is not None:
                lines.append(text)
        return "\n\n".join(lines)

    def _convert_block(self, block: Dict) -> str:
        """
        Converts a single block.
        """
        b_type = block.get('type')
        if not b_type:
            return ""

        content_obj = block.get(b_type, {})
        rich_text = content_obj.get('rich_text', [])
        text = self._render_rich_text(rich_text)
        
        # Determine markdown based on type
        if b_type == 'paragraph':
            return text
        elif b_type == 'heading_1':
            return f"# {text}"
        elif b_type == 'heading_2':
            return f"## {text}"
        elif b_type == 'heading_3':
            return f"### {text}"
        elif b_type == 'bulleted_list_item':
            return f"- {text}"
        elif b_type == 'numbered_list_item':
             return f"1. {text}" # Simple 1. for all, markdown handles numbering
        elif b_type == 'to_do':
            checked = content_obj.get('checked', False)
            mark = "x" if checked else " "
            return f"- [{mark}] {text}"
        elif b_type == 'code':
            lang = content_obj.get('language', 'text')
            return f"```{lang}\n{text}\n```"
        elif b_type == 'quote':
            return f"> {text}"
        elif b_type == 'divider':
            return "---"
        elif b_type == 'child_page':
            # Child pages shouldn't be rendered as content in the parent usually, 
            # or maybe as a link?
            # For sync, we might handle them as directory navigation later.
            title = content_obj.get('title', 'Untitled')
            return f"[{title}](subpage)" # Placeholder
        else:
            logger.debug(f"Unsupported block type for fallback: {b_type}")
            return text

    def _render_rich_text(self, rich_text: List[Dict]) -> str:
        """
        Renders rich text array to markdown string with annotations.
        """
        output = ""
        for partial in rich_text:
            plain = partial.get('plain_text', '')
            ann = partial.get('annotations', {})
            href = partial.get('href')
            
            # Apply styling
            if ann.get('code'):
                plain = f"`{plain}`"
            if ann.get('bold'):
                plain = f"**{plain}**"
            if ann.get('italic'):
                plain = f"*{plain}*"
            if ann.get('strikethrough'):
                plain = f"~~{plain}~~"
                
            # Links
            if href:
                plain = f"[{plain}]({href})"
                
            output += plain
            
        return output
