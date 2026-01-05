from typing import Dict, List, Any

class BlockValidator:
    MAX_TEXT_LENGTH = 2000

    def validate_blocks(self, blocks: List[Dict[str, Any]]) -> List[str]:
        """
        Validates a list of Notion block objects.
        Returns a list of error messages.
        """
        errors = []
        
        for i, block in enumerate(blocks):
            if not isinstance(block, dict):
                errors.append(f"Block #{i} is not a dictionary.")
                continue
                
            block_type = block.get('object')
            if block_type != 'block':
                errors.append(f"Block #{i} has invalid object type: {block_type}")
                
            type_name = block.get('type')
            if not type_name:
                errors.append(f"Block #{i} missing 'type' field.")
                continue
                
            if type_name not in block:
                errors.append(f"Block #{i} of type '{type_name}' missing content object.")
                continue
                
            content = block[type_name]
            
            # Check rich text content length
            if 'rich_text' in content:
                for j, rt in enumerate(content['rich_text']):
                    text_content = rt.get('text', {}).get('content', '')
                    if len(text_content) > self.MAX_TEXT_LENGTH:
                        errors.append(f"Block #{i} ({type_name}) item #{j}: Text exceeds {self.MAX_TEXT_LENGTH} characters.")
                        
        return errors
