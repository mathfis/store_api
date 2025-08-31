import os
import pytest
from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv('.env.local')

@pytest.fixture(scope="function")
def mongo_client():
    """Fixture síncrona do MongoDB Atlas."""
    uri = os.getenv("DATABASE_URL")
    client = MongoClient(uri, ssl=True)
    client.admin.command('ping')
    yield client
    client.close()

@pytest.fixture(scope="function")
def products_collection(mongo_client):
    """Fixture síncrona da collection products."""
    db = mongo_client.get_database()
    collection = db.products
    collection.delete_many({})
    yield collection
    collection.delete_many({})