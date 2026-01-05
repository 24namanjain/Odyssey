import uuid
from typing import Dict, List, Optional

class FrontmatterValidator:
    def validate(self, data: Dict) -> List[str]:
        """
        Validates frontmatter data.
        Returns a list of error messages.
        """
        errors = []
        
        # Check notion_page_id if present
        page_id = data.get('notion_page_id')
        if page_id:
            if not isinstance(page_id, str):
                errors.append("notion_page_id must be a string.")
            elif not self._is_valid_uuid(page_id):
                errors.append(f"Invalid notion_page_id format: {page_id}")
                
        return errors

    def _is_valid_uuid(self, val: str) -> bool:
        try:
            uuid.UUID(str(val))
            return True
        except ValueError:
            return False
