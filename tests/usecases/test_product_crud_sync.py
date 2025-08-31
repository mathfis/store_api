import pytest
from decimal import Decimal
from bson import Decimal128
from store.schemas.product import ProductIn, ProductUpdate
from store.usecases.product_sync import product_usecase_sync

def test_create_product_sync(products_collection):
    """Teste síncrono para criar produto."""
    product_data = ProductIn(
        name="Test Product",
        quantity=10,
        price=Decimal("99.99"),
        status=True
    )
    
    result = product_usecase_sync.create_sync(product=product_data)
    assert result["name"] == "Test Product"
    assert result["price"] == Decimal128('99.99')  # ← Corrigido: Decimal128

def test_list_products_sync(products_collection):
    """Teste síncrono para listar produtos."""
    product1 = ProductIn(name="Product 1", quantity=5, price=Decimal("50.00"), status=True)
    product2 = ProductIn(name="Product 2", quantity=3, price=Decimal("150.00"), status=False)
    
    product_usecase_sync.create_sync(product=product1)
    product_usecase_sync.create_sync(product=product2)
    
    result = product_usecase_sync.list_sync()
    assert len(result) == 2

def test_list_with_filters_sync(products_collection):
    """Teste síncrono para filtros."""
    products = [
        ProductIn(name="Cheap", quantity=10, price=Decimal("30.00"), status=True),
        ProductIn(name="Expensive", quantity=2, price=Decimal("300.00"), status=True),
    ]
    
    for product in products:
        product_usecase_sync.create_sync(product=product)
    
    result_min = product_usecase_sync.list_sync(min_price=50.0)
    assert len(result_min) == 1
    assert result_min[0]['name'] == 'Expensive'

def test_update_product_sync(products_collection):
    """Teste de atualização de produto."""
    product_data = ProductIn(
        name="Original Product",
        quantity=10,
        price=Decimal("100.00"),
        status=True
    )
    created = product_usecase_sync.create_sync(product_data)

    update_data = ProductUpdate(
        quantity=20,
        price=Decimal("150.00"),
        status=False
    )

    updated = product_usecase_sync.update_sync(created["_id"], update_data)
    
    assert updated is not None
    assert updated["quantity"] == 20
    assert updated["price"] == Decimal128("150.00")
    assert updated["status"] == False
    assert "updated_at" in updated

def test_update_nonexistent_product_sync(products_collection):
    """Teste de atualização de produto inexistente."""
    update_data = ProductUpdate(
        quantity=999,
        price=Decimal("999.99")
    )
    
    result = product_usecase_sync.update_sync("000000000000000000000000", update_data)
    assert result is None

def test_delete_product_sync(products_collection):
    """Teste de deleção de produto."""
    product_data = ProductIn(
        name="Product to Delete",
        quantity=5,
        price=Decimal("50.00"),
        status=True
    )
    created = product_usecase_sync.create_sync(product_data)
    
    delete_result = product_usecase_sync.delete_sync(created["_id"])
    assert delete_result is True
    
    products = product_usecase_sync.list_sync()
    assert len(products) == 0

def test_delete_nonexistent_product_sync(products_collection):
    """Teste de deleção de produto inexistente."""
    delete_result = product_usecase_sync.delete_sync("000000000000000000000000")
    assert delete_result is False