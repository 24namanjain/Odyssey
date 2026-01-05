import os
import frontmatter
from pathlib import Path

source_dir = Path("./docs")
files = list(source_dir.glob("**/*.md"))

for file_path in files:
    post = frontmatter.load(str(file_path))
    if 'notion_page_id' in post.metadata:
        del post.metadata['notion_page_id']
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(frontmatter.dumps(post))
        print(f"Cleared ID from {file_path}")
