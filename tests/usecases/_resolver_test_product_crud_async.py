import pytest
from decimal import Decimal
from store.schemas.product import ProductIn, ProductOut
from store.usecases.product import product_usecase

@pytest.mark.asyncio
async def test_create_product_integration(products_collection):
    """Teste de integração para criar produto."""
    product_data = ProductIn(
        name="Test Product",
        quantity=10,
        price=Decimal("99.99"),
        status=True
    )
    
    result = await product_usecase.create(product=product_data)
    assert isinstance(result, ProductOut)
    assert result.name == "Test Product"
    assert result.price == Decimal("99.99")

@pytest.mark.asyncio
async def test_list_products_integration(products_collection):
    """Teste de integração para listar produtos."""
    # Cria dois produtos de teste
    product1 = ProductIn(name="Product 1", quantity=5, price=Decimal("50.00"), status=True)
    product2 = ProductIn(name="Product 2", quantity=3, price=Decimal("150.00"), status=False)
    
    await product_usecase.create(product=product1)
    await product_usecase.create(product=product2)
    
    # Testa listagem sem filtros
    result = await product_usecase.list()
    assert len(result) == 2
    assert all(isinstance(item, ProductOut) for item in result)

@pytest.mark.asyncio
async def test_list_with_filters_integration(products_collection):
    """Teste de integração para filtros."""
    # Cria produtos com preços variados
    products = [
        ProductIn(name="Cheap", quantity=10, price=Decimal("30.00"), status=True),
        ProductIn(name="Expensive", quantity=2, price=Decimal("300.00"), status=True),
        ProductIn(name="Inactive", quantity=5, price=Decimal("100.00"), status=False)
    ]
    
    for product in products:
        await product_usecase.create(product=product)
    
    # Testa filtro de preço mínimo
    result_min = await product_usecase.list(min_price=50.0)
    assert len(result_min) == 2  # Expensive + Inactive
    
    # Testa filtro de status
    result_active = await product_usecase.list(status=True)
    assert len(result_active) == 2  # Cheap + Expensive

@pytest.mark.asyncio
async def test_get_product_integration(products_collection):
    """Teste de integração para obter produto por ID."""
    product_data = ProductIn(
        name="Test Get",
        quantity=15,
        price=Decimal("75.50"),
        status=True
    )
    
    created = await product_usecase.create(product=product_data)
    
    # Busca o produto criado
    result = await product_usecase.get(id=created.id)
    assert result.name == "Test Get"
    assert result.quantity == 15

@pytest.mark.asyncio
async def test_update_product_integration(products_collection):
    """Teste de integração para atualizar produto."""
    product_data = ProductIn(
        name="Original",
        quantity=10,
        price=Decimal("100.00"),
        status=True
    )
    
    created = await product_usecase.create(product=product_data)
    
    # Atualiza o produto
    updated = await product_usecase.update(
        id=created.id,
        quantity=20,
        price=Decimal("150.00"),
        status=False
    )
    
    assert updated.quantity == 20
    assert updated.price == Decimal("150.00")
    assert updated.status is False

@pytest.mark.asyncio
async def test_delete_product_integration(products_collection):
    """Teste de integração para deletar produto."""
    product_data = ProductIn(
        name="To Delete",
        quantity=5,
        price=Decimal("50.00"),
        status=True
    )
    
    created = await product_usecase.create(product=product_data)
    
    # Deleta o produto
    await product_usecase.delete(id=created.id)
    
    # Verifica que foi deletado
    result = await product_usecase.list()
    assert len(result) == 0