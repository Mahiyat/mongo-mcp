import os
import json
from pymongo import MongoClient
from mcp.server.fastmcp import FastMCP
from typing import Union, Optional
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,  # Set to INFO or DEBUG as needed
    format="%(asctime)s [%(levelname)s] %(message)s"
)

mcp = FastMCP("mongo_toolkit")

logging.info(f"All environment variables: {dict(os.environ)}")
# Read Mongo URI from environment
# mongo_uri = os.getenv("MONGO_URI")
# mongo_db = os.getenv("MONGO_DB")
# if not mongo_uri or not mongo_db:
#     raise Exception("Invalid Mongo URI or MONGO DB!")
mongo_uri = 'mongodb://admin:password@mongo:27017'

logging.info(mongo_uri)
try:
    client = MongoClient(mongo_uri)
except Exception as e:
    raise e

db = client['mcp-db']
collection = db["courses"]
# Log the values
logging.info(f"Database: {db}")
logging.info(f"Collection: {collection}")

@mcp.tool()
async def find_documents(filter_json: dict = '{}', limit: Optional[int] = 5) -> str:
    try:
        # Handle both string and dict input for filter_json
        if isinstance(filter_json, dict):
            query_filter = filter_json
        else:
            query_filter = json.loads(filter_json)
        
        print(f"Query Filter: {query_filter}")
        cursor = collection.find(query_filter)
        if limit is not None and limit > 0:  # Only apply limit if provided and positive
            cursor = cursor.limit(limit)
        
        results = [doc for doc in cursor]
        for doc in results:
            doc["_id"] = str(doc["_id"])
        return json.dumps(results, indent=2)
    except Exception as e:
        return f"Error: {str(e)}"

@mcp.tool()
async def insert_document(document_json: dict) -> str:
    try:
        document = json.loads(document_json)
        print(document)
        result = collection.insert_one(document)
        return f"Inserted document with _id: {str(result.inserted_id)}"
    except Exception as e:
        return f"Error: {str(e)}"

@mcp.tool()
async def delete_documents(filter_json: str) -> str:
    try:
        query_filter = json.loads(filter_json)
        result = collection.delete_many(query_filter)
        return f"Deleted {result.deleted_count} document(s)"
    except Exception as e:
        return f"Error: {str(e)}"

if __name__ == "__main__":
    mcp.run(transport="stdio")
