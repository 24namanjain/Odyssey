from typing import List, Tuple, Optional
from markdown_it import MarkdownIt

class MarkdownValidator:
    def __init__(self):
        # We enable tables (and other GFM features) so that the parser recognizes them as specific tokens.
        # This allows us to explicitly catch 'table_open' and forbid it.
        self.md = MarkdownIt('gfm-like')
        # Unsupported token types map to user-friendly messages
        self.unsupported_tokens = {
            'table_open': 'Tables are not supported.',
            'html_block': 'HTML blocks are not supported.',
            'html_inline': 'Inline HTML is not supported.',
            # Embeds usually appear as specific tokens or html, but simple embeds might need custom checks depending on plugin usage.
            # For standard markdown-it, we focus on what map supports.
        }

    def validate(self, content: str) -> List[str]:
        """
        Validates markdown content.
        Returns a list of error messages. Empty list means valid.
        """
        errors = []
        
        # 1. Check for empty content
        if not content.strip():
            errors.append("Markdown content is empty.")
            return errors

        # 2. Parse tokens to check for unsupported constructs
        tokens = self.md.parse(content)
        
        for token in tokens:
            if token.type in self.unsupported_tokens:
                errors.append(f"Line {token.map[0] if token.map else '?'}: {self.unsupported_tokens[token.type]}")
                
            # Warn on long paragraphs (we'll log this in the main loop, but here we can just note it or strict fail if needed. 
            # Requirements say "Warn (do not fail)". The validator returns errors, so maybe we need a separate warning mechanism?
            # For now, let's keep errors strict. We can expose warnings separately or strict fail on errors only.
        
        return errors

    def check_warnings(self, content: str) -> List[str]:
        """
        Checks for non-blocking warnings.
        """
        warnings = []
        tokens = self.md.parse(content)
        
        for token in tokens:
            if token.type == 'inline':
                # content is in the children usually for inline, but token.content holds the text
                if len(token.content) > 2000:
                    warnings.append(f"Line {token.map[0] if token.map else '?'}: Paragraph exceeds 2000 characters recommendation.")
                    
        return warnings
