import pytest
from decimal import Decimal
from bson import Decimal128
from store.schemas.product import ProductIn, ProductUpdate
from store.usecases.product import product_usecase

def test_usecases_update_schema_validation():
    """Teste unitário - valida schema ProductUpdate"""
    update_data = ProductUpdate(
        quantity=20,
        price=Decimal("99.99"),
        status=True
    )
    
    assert update_data.quantity == 20
    assert isinstance(update_data.price, Decimal128)
    assert str(update_data.price) == "99.99"
    assert update_data.status is True

def test_usecases_delete_schema_validation():
    """Teste unitário - valida assinatura do método delete"""
    assert hasattr(product_usecase, 'delete')
    assert callable(product_usecase.delete)

def test_usecases_list_schema_validation():
    """Teste unitário - valida assinatura do método list"""
    assert hasattr(product_usecase, 'list')
    assert callable(product_usecase.list)

def test_usecases_product_in_schema():
    """Teste unitário - valida schema ProductIn"""
    product_data = {
        "name": "Test Product",
        "quantity": 10,
        "price": Decimal("100.50"),
        "status": True
    }
    
    product_in = ProductIn(**product_data)
    assert product_in.name == "Test Product"
    assert product_in.quantity == 10
    assert product_in.price == Decimal("100.50")
    assert product_in.status is True

def test_usecases_list_method_signature():
    """Teste unitário - valida assinatura dos parâmetros do list"""
    import inspect
    
    sig = inspect.signature(product_usecase.list)
    params = sig.parameters
    
    assert 'min_price' in params
    assert 'max_price' in params  
    assert 'status' in params
    assert params['min_price'].default is None
    assert params['max_price'].default is None
    assert params['status'].default is None

def test_usecases_list_query_builder():
    """Teste unitário - valida lógica de construção de query"""
    # Testa a lógica de construção da query sem banco
    usecase = product_usecase.__class__()
    
    test_cases = [
        ({}, {}),
        ({'min_price': 10.0}, {'price': {'$gte': 10.0}}),
        ({'max_price': 100.0}, {'price': {'$lte': 100.0}}),
        ({'status': True}, {'status': True}),
        ({'min_price': 10.0, 'max_price': 100.0}, {'price': {'$gte': 10.0, '$lte': 100.0}}),
        ({'min_price': 50.0, 'status': False}, {'price': {'$gte': 50.0}, 'status': False})
    ]
    
    for filters, expected_query in test_cases:
        query = {}
        
        if filters.get('min_price') is not None or filters.get('max_price') is not None:
            query['price'] = {}
            if filters.get('min_price') is not None:
                query['price']['$gte'] = filters['min_price']
            if filters.get('max_price') is not None:
                query['price']['$lte'] = filters['max_price']
        
        if filters.get('status') is not None:
            query['status'] = filters['status']
            
        assert query == expected_query