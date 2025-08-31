# \store\controllers\product.py
from fastapi import APIRouter, HTTPException, status
from store.schemas.product import ProductIn, ProductOut, ProductUpdate
from store.usecases.product import product_usecase

def handle_usecase_exceptions(func):
    """
    Envelope que captura exceções dos usecases e converte para HTTPException.
    """
    async def envelope(*args, **kwargs):
        try:
            return await func(*args, **kwargs)
        except Exception as e:
            if "not found" in str(e).lower():
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=str(e) or "Recurso não encontrado"
                )
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Erro interno do servidor: {str(e)}"
            )
    return envelope

router = APIRouter(prefix="/products", tags=["Products"])

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=ProductOut)
@handle_usecase_exceptions
async def criar_produto(product_in: ProductIn):
    """
    Cria um novo produto.
    
    Args:
        product_in: Dados do produto validados pelo schema ProductIn
        
    Returns:
        ProductOut: Produto criado com ID e datas geradas
    """
    resultado = await product_usecase.create(product_in)
    return resultado

@router.get("/{id}", response_model=ProductOut)
@handle_usecase_exceptions
async def buscar_produto(id: str):
    """
    Busca um produto pelo ID.
    
    Args:
        id: ID do produto (string do MongoDB)
        
    Returns:
        ProductOut: Dados completos do produto
    """
    resultado = await product_usecase.get(id)
    return resultado

@router.put("/{id}", response_model=ProductOut)
@handle_usecase_exceptions
async def atualizar_produto(id: str, product_update: ProductUpdate):
    """
    Atualiza um produto existente.
    
    Args:
        id: ID do produto a ser atualizado
        product_update: Campos a serem atualizados (parciais)
        
    Returns:
        ProductOut: Produto atualizado
    """
    resultado = await product_usecase.update(id, product_update)
    return resultado

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
@handle_usecase_exceptions
async def deletar_produto(id: str):
    """
    Remove um produto pelo ID.
    
    Args:
        id: ID do produto a ser removido
    """
    await product_usecase.delete(id)

@router.get("/", response_model=list[ProductOut])
@handle_usecase_exceptions
async def listar_produtos(
    preco_minimo: float = None,
    preco_maximo: float = None,
    status: bool = None
):
    """
    Lista produtos com filtros opcionais.
    
    Args:
        preco_minimo: Filtro de preço mínimo (parâmetro de query)
        preco_maximo: Filtro de preço máximo (parâmetro de query) 
        status: Filtro de status (parâmetro de query)
        
    Returns:
        list[ProductOut]: Lista de produtos que atendem aos filtros
    """
    resultado = await product_usecase.list(
        min_price=preco_minimo,
        max_price=preco_maximo,
        status=status
    )
    return resultado