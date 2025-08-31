# Store API - TDD com FastAPI + MongoDB

## 📋 Fase 1: Configuração do Ambiente

### Pré-requisitos
- Python 3.11.9
- Poetry (gerenciador de pacotes)
- Conta MongoDB Atlas (banco em nuvem)

### 1. Instalação do Poetry
```bash
pip install poetry
```
### 2. Criar Projeto

```bash
# Navegar para diretório desejado
cd C:\Users\seu_usuario\seu_diretorio

# Criar projeto com Poetry
poetry new store-api
cd store-api
```
### 3. Configurar Dependências (pyproject.toml)
```toml
[project]
name = "store-api"
version = "0.1.0"
description = "Projeto de aprendizado de TDD usando MongoDB"
authors = [
    {name = "seu_nome", email = "seu_email@gmail.com"}
]
license = {text = "MIT"}
readme = "README.md"
requires-python = "3.11.9"

[tool.poetry.dependencies]
python = "3.11.9"
fastapi = "0.116.1"
uvicorn = "0.35.0"
pydantic = "2.11.7"
pydantic-settings = "2.10.1"
motor = "3.7.1"
pytest = "8.4.1"
pytest-asyncio = "1.1.0"
pre-commit = "4.3.0"

[build-system]
requires = ["poetry-core>=2.0.0,<3.0.0"]
build-backend = "poetry.core.masonry.api"
```
### 4. Instalar Dependências
```bash
# Instalar sem erro de pacote root
poetry install --no-root
```
### 5. Ativar Ambiente Virtual
```bash
# Poetry 2.0+ 
poetry env activate

# Verificar se funcionou
python --version
# Deve mostrar: Python 3.11.x
```
### ✅ Verificação Final
```bash
# Listar pacotes (Windows PowerShell)
poetry run pip list | Select-String "fastapi|motor|pydantic"

# Listar pacotes (Git Bash/Linux)
poetry run pip list | grep -E "fastapi|motor|pydantic"
```
saída:
```text
fastapi            0.116.1
motor              3.7.1
pydantic           2.11.7
pydantic_core      2.33.2
pydantic-settings  2.10.1

```
## ✅ Funcionalidades Implementadas
CRUD Completo de Produtos
POST /products - Criar produto

GET /products - Listar produtos (com filtros)

GET /products/{id} - Obter produto por ID

PATCH /products/{id} - Atualizar produto parcialmente

DELETE /products/{id} - Remover produto

Filtros de Busca
min_price: Valor mínimo

max_price: Valor máximo

status: Status do produto (True/False)

Combinações: Filtros múltiplos simultâneos

Schemas Pydantic Validados
ProductIn: Schema para criação

ProductOut: Schema para resposta

ProductUpdate: Schema para atualização

🧪 Suíte de Testes
Estatísticas Atuais
✅ 14 testes passando (100% de sucesso)

📊 55% de cobertura total

⚡ 68 segundos de execução

Distribuição dos Testes
bash
tests/
├── usecases/
│   ├── test_product.py              # 7 testes unitários (async)
│   └── test_product_crud_sync.py    # 7 testes integração (síncrono)
Cobertura por Módulo
store/usecases/product_sync.py: 95% ✅

store/schemas/product.py: 100% ✅

store/schemas/base.py: 57% ⚠️

store/usecases/product.py: 34% ⚠️

store/controllers/product.py: 0% ❌

🚦 Solução Técnica Implementada
Problema Resolvido: "Event Loop is Closed"
Causa: Conflito entre motor (async) e pytest-asyncio no Windows + Python 3.11

Solução: Arquitetura híbrida:

🎯 Produção: Async completo (FastAPI + Motor)

🧪 Testes: Sync para integração (pymongo + fixtures)

Fixtures MongoDB para Testes
python
# tests/conftest.py
@pytest.fixture(scope="function")
def products_collection(mongo_client):
    db = mongo_client.get_database()
    collection = db.products
    collection.delete_many({})  # Limpeza entre testes
    yield collection
    collection.delete_many({})
Usecase Síncrono para Testes
python
# store/usecases/product_sync.py
class ProductUsecaseSync:
    def create_sync(self, product: ProductIn) -> dict: ...
    def list_sync(self, **filters) -> list: ...
    def update_sync(self, id: str, product: ProductUpdate) -> dict: ...
    def delete_sync(self, id: str) -> bool: ...
🎯 Próximas Etapas (Desafio Final)
⏳ Itens em Andamento
Exceções customizadas (NotFoundError, InsertError)

Tratamento na controller com mensagens amigáveis

updated_at automático nas atualizações

❌ Itens Pendentes
Testes de controllers (cobertura atual: 0%)

Validação de filtros combinados avançados

Documentação OpenAPI completa

🎯 Metas para 24h
Atingir >70% de cobertura total

Implementar testes de controllers

Completar tratamento de exceções

🚀 Como Executar
1. Instalação
bash
git clone <repositorio>
cd store_api
poetry install --no-root
2. Configuração de Ambiente
bash
# Criar arquivo .env.local
echo "MONGODB_ATLAS_URI=mongodb+srv://usuario:senha@cluster.mongodb.net/" > .env.local
3. Execução dos Testes
bash
make test
# ou
poetry run pytest --cov=store tests/ --cov-report=term-missing
4. Execução da API
bash
poetry run uvicorn store.main:app --reload
📊 Decisões Técnicas Documentadas
Arquitetura Híbrida (Async/Sync)
Decisão: Priorizar entrega funcional com testes robustos sobre pureza arquitetural

Vantagens:

✅ Desbloqueia desenvolvimento imediato

✅ Mantém validação real com MongoDB Atlas

✅ Permite evolução para async futuro

Justificativa: "O bloqueio técnico do event loop impedia progresso. A solução híbrida mantém a qualidade da aplicação enquanto garante entrega dentro do prazo do bootcamp."

👨‍💻 Desenvolvido por
Matheus Lara - Bootcamp Santander 2025 - DIO

📄 Licença
MIT License - veja o arquivo LICENSE para detalhes.

✅ ENTREGA PARCIAL CONCLUÍDA - PRÓXIMA FASE: STORE_API - CONTROLLERS