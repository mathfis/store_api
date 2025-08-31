from datetime import datetime
import os
from dotenv import load_dotenv
from pymongo import MongoClient
from store.schemas.product import ProductIn, ProductUpdate
from bson import ObjectId, Decimal128

load_dotenv('.env.local')

class ProductUsecaseSync:
    def __init__(self) -> None:
        uri = os.getenv("DATABASE_URL")
        self.client = MongoClient(uri, ssl=True)
        self.db = self.client.get_database()
        self.collection = self.db.products

    def create_sync(self, product: ProductIn) -> dict:
        product_dict = product.model_dump()
        product_dict["price"] = Decimal128(str(product_dict["price"]))
        result = self.collection.insert_one(product_dict)
        return self.collection.find_one({"_id": result.inserted_id})

    def list_sync(self, min_price: float = None, max_price: float = None, status: bool = None) -> list:
        query = {}
        if min_price is not None or max_price is not None:
            query["price"] = {}
            if min_price is not None:
                query["price"]["$gte"] = min_price
            if max_price is not None:
                query["price"]["$lte"] = max_price
        if status is not None:
            query["status"] = status
        return list(self.collection.find(query))

    def delete_sync(self, id: str) -> bool:
        """Versão síncrona do delete."""
        result = self.collection.delete_one({"_id": ObjectId(id)})
        return result.deleted_count > 0
    
    def update_sync(self, id: str, product: ProductUpdate) -> dict:
        """Versão síncrona do update."""
        update_data = product.model_dump(exclude_unset=True)
        
        if "price" in update_data:
            update_data["price"] = Decimal128(str(update_data["price"]))
        
        update_data["updated_at"] = datetime.now()
        
        result = self.collection.update_one(
            {"_id": ObjectId(id)},
            {"$set": update_data}
        )
        
        if result.matched_count == 0:
            return None
        
        return self.collection.find_one({"_id": ObjectId(id)})
    
product_usecase_sync = ProductUsecaseSync()