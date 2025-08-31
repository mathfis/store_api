from datetime import datetime
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from store.db.mongo import db_client
from store.schemas.product import ProductIn, ProductOut, ProductUpdate
from bson import ObjectId
from fastapi import HTTPException, status

class ProductUsecase:
    def __init__(self) -> None:
        self.client: AsyncIOMotorClient = db_client.get()
        self.database: AsyncIOMotorDatabase = self.client.get_database()
        self.collection = self.database.get_collection("products")

    async def create(self, product: ProductIn) -> ProductOut:
        product_data = product.model_dump()
        product_data["price"] = float(product_data["price"])
        result = await self.collection.insert_one(product_data)
        new_product = await self.collection.find_one({"_id": result.inserted_id})
        return ProductOut(**new_product)

    async def update(self, id: str, product: ProductUpdate) -> ProductOut:
        update_data = product.model_dump(exclude_none=True)
        
        if "price" in update_data:
            update_data["price"] = float(update_data["price"])
        
        update_data["updated_at"] = datetime.now()
        
        result = await self.collection.update_one(
            {"_id": ObjectId(id)},
            {"$set": update_data}
        )
        
        if result.matched_count == 0:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Produto não encontrado"
            )
        
        updated_product = await self.collection.find_one({"_id": ObjectId(id)})
        return ProductOut(**updated_product)

    async def get(self, id: str) -> ProductOut:
        result = await self.collection.find_one({"_id": ObjectId(id)})
        if not result:
            raise HTTPException(status_code=404, detail="Product not found")
        return ProductOut(**result)

    async def delete(self, id: str) -> bool:
        result = await self.collection.delete_one({"_id": ObjectId(id)})
        
        if result.deleted_count == 0:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Produto não encontrado"
            )
        
        return True

    async def list(self, min_price: float = None, max_price: float = None, status: bool = None) -> list[ProductOut]:
        query = {}
        
        if min_price is not None or max_price is not None:
            query["price"] = {}
            if min_price is not None:
                query["price"]["$gte"] = min_price
            if max_price is not None:
                query["price"]["$lte"] = max_price
        
        if status is not None:
            query["status"] = status
        
        products = await self.collection.find(query).to_list(length=None)
        return [ProductOut(**product) for product in products]

product_usecase = ProductUsecase()