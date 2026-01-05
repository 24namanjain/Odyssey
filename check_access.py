import os
import sys
from dotenv import load_dotenv
from notion_client import Client

# Force load .env
load_dotenv()

token = os.environ.get("NOTION_TOKEN")
db_id = os.environ.get("NOTION_DATABASE_ID")

if not token:
    print("No token provided in .env")
    sys.exit(1)

notion = Client(auth=token)

try:
    print(f"Using token: {token[:4]}...{token[-4:]}")
    print(f"Target DB ID: {db_id}")
    
    # Search for everything
    response = notion.search()
    results = response.get("results", [])
    
    dbs = [r for r in results if r["object"] == "database"]
    
    print(f"Total results: {len(results)}")
    for res in results:
        obj_type = res.get("object")
        title = "Untitled"
        
        # Get title based on type (Database has 'title', Page has 'properties' -> 'title')
        if obj_type == "database":
             if res.get("title") and len(res["title"]) > 0:
                title = res["title"][0].get("plain_text", "Untitled")
        elif obj_type == "page":
             # Pages titles are in properties. It's complex to extract generically.
             # Just try to get it if simpler.
             # Or just print ID and type.
             pass
             
        print(f"Found {obj_type}: {res['id']}")
        
    if db_id:
        # Try to retrieve specific DB
        try:
            db = notion.databases.retrieve(database_id=db_id)
            title = "Untitled"
            if db.get("title") and len(db["title"]) > 0:
                title = db["title"][0].get("plain_text", "Untitled")
            print(f"SUCCESS: Successfully retrieved target database: {title}")
        except Exception as e:
            print(f"FAILURE: Could not retrieve target database {db_id}: {e}")

except Exception as e:
    print(f"Error: {e}")
