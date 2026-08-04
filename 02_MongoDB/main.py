from fastapi import FastAPI
from motor.motor_asyncio import AsyncIOMotorClient
from pydantic import BaseModel
from bson import ObjectId
import os
from dotenv import load_dotenv
from urllib.parse import quote

load_dotenv()

username = os.getenv("MONGO_USERNAME")
password = quote(os.getenv("MONGO_PASSWORD"), safe='')  # URL-encodes special chars
hostname = os.getenv("MONGO_HOSTNAME")
db_name = os.getenv("MONGO_DATABASE")

mongo_url = f"mongodb+srv://{username}:{password}@{hostname}/?appName={db_name}"

client = AsyncIOMotorClient(mongo_url)
db = client["euron"]
euron_data = db["euron_collection"]

app = FastAPI()

class EuronData(BaseModel):
    name: str
    phone: int
    city: str
    course: str

@app.post("/euron/insert")
async def euron_data_insert_helper(data:EuronData):
    result = await euron_data.insert_one(data.dict())
    return str(result.inserted_id)

def euron_data_helper(doc):
    doc["id"] = str(doc["_id"])
    del doc["_id"]
    return doc

@app.get("/euron/getdata")
async def euron_data_get_helper():
    items = []
    cursor = euron_data.find({})
    async for document in cursor:
        items.append(euron_data_helper(document))
    return items
