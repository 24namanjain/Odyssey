from typing import List, Dict, Any, Tuple
import frontmatter
from markdown_it import MarkdownIt
from markdown_it.token import Token

class MarkdownParser:
    def __init__(self):
        self.md = MarkdownIt()

    def parse_file(self, file_path: str) -> Tuple[Dict, List[Dict[str, Any]]]:
        """
        Parses a markdown file and returns frontmatter and Notion blocks.
        """
        with open(file_path, 'r', encoding='utf-8') as f:
            post = frontmatter.load(f)
            
        md_content = post.content
        metadata = post.metadata
        
        blocks = self.convert_to_blocks(md_content)
        return metadata, blocks

    def convert_to_blocks(self, content: str) -> List[Dict[str, Any]]:
        tokens = self.md.parse(content)
        blocks = []
        
        i = 0
        while i < len(tokens):
            token = tokens[i]
            
            if token.type == 'heading_open':
                # Handle headings
                level = int(token.tag[1])
                # Only h1, h2, h3 supported
                if level > 3:
                    level = 3
                
                # Get inline content
                i += 1
                inline_token = tokens[i]
                text_content = self._parse_inline(inline_token)
                
                block_type = f"heading_{level}"
                blocks.append({
                    "object": "block",
                    "type": block_type,
                    block_type: {
                        "rich_text": text_content
                    }
                })
                # Skip heading_close
                i += 1
                
            elif token.type == 'paragraph_open':
                # Handle paragraphs
                i += 1
                inline_token = tokens[i] 
                
                # Check for hidden conversion cases like images (not supported)
                # But we validated against unsupported types.
                
                text_content = self._parse_inline(inline_token)
                
                # If paragraph contains only an image, it might be unsupported
                # But for now assuming valid text
                if text_content: # Only add if not empty
                    blocks.append({
                        "object": "block",
                        "type": "paragraph",
                        "paragraph": {
                            "rich_text": text_content
                        }
                    })
                i += 1
                
            elif token.type == 'bullet_list_open' or token.type == 'ordered_list_open':
                # We process list items inside
                # But actually markdown-it structure is flattened list of tokens
                # We can just iterate.
                pass 
                
            elif token.type == 'list_item_open':
                # We need to know if it's ordered or bullet
                # Look at previous token or parent context? 
                # Markdown-it tokens are linear.
                # Actually, simpler: check the surrounding list_open token markup
                # A robust way is to track state or just look at the token markup
                
                # But wait, we iterate linear. 'list_item_open' is followed by 'paragraph_open' usually for the content.
                # Let's peek ahead.
                
                # Ideally we need context of the list type.
                # Let's handle this by iterating carefully or using a stack.
                pass 

            elif token.type == 'fence':
                # Code block
                lang = token.info.strip()
                # Notion languages are specific, defaulting to plain text if unknown or empty
                # For simplicity, pass commonly used ones or default
                
                blocks.append({
                    "object": "block",
                    "type": "code",
                    "code": {
                        "rich_text": [{"type": "text", "text": {"content": token.content}}],
                        "language": lang if lang else "plain text"
                    }
                })
                
            elif token.type == 'hr':
                blocks.append({
                    "object": "block",
                    "type": "divider",
                    "divider": {}
                })
                
            i += 1
            
        # Re-implement list parsing because linear scan is tricky with nesting
        # Actually for a first pass, let's use a simpler heuristic or a proper nested walker.
        # Given constraints, I will rewrite convert_to_blocks to handle lists more robustly.
        return blocks

    def _parse_inline(self, token: Token) -> List[Dict]:
        """
        Parses inline children tokens into Notion rich_text objects.
        """
        if not token.children:
            return []
            
        rich_text = []
        
        for child in token.children:
            if child.type == 'text':
                rich_text.append({
                    "type": "text",
                    "text": {"content": child.content}
                })
            elif child.type == 'code_inline':
                rich_text.append({
                    "type": "text",
                    "text": {"content": child.content},
                    "annotations": {"code": True}
                })
            elif child.type == 'link_open':
                # We need the href. It's in attrs.
                href = None
                for k, v in child.attrs.items():
                    if k == 'href':
                        href = v
                        break
                
                # The next token should be text, then link_close
                # structure: link_open, text (or others), link_close
                # This simple loop might fail for nested inlines inside link.
                # But standard markdown usually: text inside link.
                
                # We can set a "pending link" state?
                # For simplicity, let's assume flat structure or handle it in the next iteration?
                # Actually, 'child' is an inline token. child.children is null usually.
                # Wait, token.children is the list of inline tokens.
                # So we are iterating over them.
                pass
            
            # This inline parser needs to be robust for formatting (bold, italic) 
            # and links.
            # Given constraints and "no framework", doing a full AST traversal is safer.
        
        # Rewriting _parse_inline to handle styles properly
        return self._process_inline_tokens(token.children)
        
    def _process_inline_tokens(self, tokens: List[Token]) -> List[Dict]:
        result = []
        current_style = {
            "bold": False,
            "italic": False,
            "strikethrough": False,
            "code": False,
            "url": None
        }
        
        for token in tokens:
            if token.type == 'text':
                self._append_text(result, token.content, current_style)
            
            elif token.type == 'code_inline':
                # Code overrides other styles usually, or adds to them (Notion supports bold code)
                # But usually code inline is just monospaced
                style = current_style.copy()
                style['code'] = True
                self._append_text(result, token.content, style)
                
            elif token.type == 'strong_open':
                current_style['bold'] = True
            elif token.type == 'strong_close':
                current_style['bold'] = False
                
            elif token.type == 'em_open':
                current_style['italic'] = True
            elif token.type == 'em_close':
                current_style['italic'] = False
                
            elif token.type == 's_open': # Strikethrough? Markdown-it uses 's' usually?
                # Check markdown-it documentation or defaults. It creates s_open for ~~
                current_style['strikethrough'] = True
            elif token.type == 's_close':
                current_style['strikethrough'] = False
                
            elif token.type == 'link_open':
                href = token.attrGet('href')
                current_style['url'] = href
            elif token.type == 'link_close':
                current_style['url'] = None
                
        return result

    def _append_text(self, result_list, text, style):
        if not text:
            return
            
        annotations = {
            "bold": style['bold'],
            "italic": style['italic'],
            "strikethrough": style['strikethrough'],
            "code": style['code'],
            "underline": False,
            "color": "default"
        }
        
        item = {
            "type": "text",
            "text": {
                "content": text
            },
            "annotations": annotations
        }
        
        if style['url']:
            url = style['url']
            # Notion requires valid absolute URLs. 
            # We skip relative links or anchors for now to prevent API errors.
            if url.startswith("http://") or url.startswith("https://"):
                item["text"]["link"] = {"url": url}
            # else: log warning if possible, but we just skip to be safe.
            
        result_list.append(item)

    def convert_to_blocks(self, content: str) -> List[Dict[str, Any]]:
        tokens = self.md.parse(content)
        return self._tokens_to_blocks(tokens)
        
    def _tokens_to_blocks(self, tokens: List[Token]) -> List[Dict[str, Any]]:
        # Root container
        root = {"children": []}
        stack = [root]
        
        # Track list type separately because 'list_item_open' doesn't say if it's bullet or ordered
        # We push 'bulleted_list_item' or 'numbered_list_item' to this stack on list_open
        list_type_stack = [] 
        
        i = 0
        while i < len(tokens):
            token = tokens[i]
            
            if token.type == 'heading_open':
                level = int(token.tag[1])
                level = min(max(level, 1), 3)
                block_type = f"heading_{level}"
                
                # Get content
                i += 1
                inline = tokens[i]
                rich_text = self._process_inline_tokens(inline.children)
                
                block = {
                    "object": "block",
                    "type": block_type,
                    block_type: {"rich_text": rich_text}
                }
                
                # Headings are always root-levelish (or children of current container)
                self._add_block(stack[-1], block)
                
                i += 1 # heading_close
            
            elif token.type == 'paragraph_open':
                # Check if we are inside a list item that needs content
                parent = stack[-1]
                
                # Handling paragraph content
                i += 1
                inline = tokens[i]
                rich_text = self._process_inline_tokens(inline.children)
                
                if self._is_list_item(parent) and not self._has_content(parent):
                    # Assign to the list item itself
                    type_name = parent['type']
                    parent[type_name]['rich_text'] = rich_text
                else:
                    # It's a standalone paragraph block (or secondary paragraph in list)
                    # For Notion, secondary paragraphs in a list item should be children blocks (paragraphs)
                    # of that list item.
                    block = {
                        "object": "block",
                        "type": "paragraph",
                        "paragraph": {"rich_text": rich_text}
                    }
                    self._add_block(parent, block)
                    
                i += 1 # paragraph_close
                
            elif token.type == 'bullet_list_open':
                list_type_stack.append('bulleted_list_item')
                
            elif token.type == 'ordered_list_open':
                list_type_stack.append('numbered_list_item')
                
            elif token.type == 'bullet_list_close' or token.type == 'ordered_list_close':
                if list_type_stack:
                    list_type_stack.pop()
                    
            elif token.type == 'list_item_open':
                # Create the list item block
                block_type = list_type_stack[-1] if list_type_stack else 'bulleted_list_item'
                
                block = {
                    "object": "block",
                    "type": block_type,
                    block_type: {
                        "rich_text": [], # Will be filled by subsequent paragraph
                        "children": []
                    }
                }
                
                self._add_block(stack[-1], block)
                stack.append(block) # Enter this block context
                
            elif token.type == 'list_item_close':
                # Leave block context
                # Clean up if no content? Notion fails if rich_text is empty? 
                # Usually markdown-it list item has content.
                if len(stack) > 1: # Don't pop root
                    stack.pop()

            elif token.type == 'fence':
                lang = token.info.strip().split()[0] if token.info.strip() else "plain text"
                block = {
                    "object": "block",
                    "type": "code",
                    "code": {
                        "rich_text": [{"type": "text", "text": {"content": token.content}}],
                        "language": lang
                    }
                }
                self._add_block(stack[-1], block)
                
            elif token.type == 'hr':
                block = {"object": "block", "type": "divider", "divider": {}}
                self._add_block(stack[-1], block)

            # Ignore others
            i += 1

        blocks = root['children']
        self._remove_empty_children(blocks)
        return blocks

    def _remove_empty_children(self, blocks: List[Dict]):
        """
        Recursively removes 'children' keys if they are empty lists,
        as Notion API sometimes rejects them (validation error).
        """
        for block in blocks:
            code_type = block.get('type')
            if code_type and code_type in block:
                content = block[code_type]
                if 'children' in content:
                    # Recurse first
                    self._remove_empty_children(content['children'])
                    # If empty after recursion, remove it
                    if not content['children']:
                        del content['children']
    def _add_block(self, parent: Dict, block: Dict):
        # Case 1: Parent is the abstract Root container
        if 'children' in parent and 'type' not in parent:
            parent['children'].append(block)
            return

        # Case 2: Parent is a Notion Block
        block_type = parent.get('type')
        if block_type and block_type in parent:
            # e.g. parent['bulleted_list_item']['children']
            container = parent[block_type]
            if 'children' in container:
                container['children'].append(block)
            else:
                # Block type doesn't have children initialized
                pass

    def _is_list_item(self, block: Dict) -> bool:
        return block.get('type') in ['bulleted_list_item', 'numbered_list_item']

    def _has_content(self, block: Dict) -> bool:
        # Check if rich_text is populated
        t = block.get('type')
        if t and block.get(t, {}).get('rich_text'):
            return True
        return False
