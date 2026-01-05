import os
import json
from dotenv import load_dotenv
from notion_client import Client

load_dotenv()
token = os.environ.get("NOTION_TOKEN")
db_id = os.environ.get("NOTION_DATABASE_ID")
notion = Client(auth=token)

try:
    # generic query
    response = notion.databases.query(database_id=db_id, page_size=1)
    results = response['results']
    if not results:
        print("No pages found.")
    else:
        page = results[0]
        # Print properties keys to see if we can read title
        print(f"Page ID: {page['id']}")
        print(f"Properties keys: {list(page['properties'].keys())}")
        
        # Try to extract title
        # Usually properties['Name'] or properties['title']
        # We need to find the 'title' type property
        title_prop = None
        for name, prop in page['properties'].items():
            if prop['id'] == 'title':
                 title_prop = name
                 break
        
        print(f"Title Property Name: {title_prop}")
        if title_prop:
             print(f"Title content: {page['properties'][title_prop]}")
             
except Exception as e:
    print(e)

