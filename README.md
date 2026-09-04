# Mini Mercado Livre

API REST de um marketplace simplificado, desenvolvida com FastAPI para estudo prático de arquitetura Back-End, regras de negócio, persistência de dados e testes automatizados.

O projeto começa como um monolito organizado em camadas e será evoluído gradualmente para uma arquitetura baseada em microsserviços e mensageria.

## Funcionalidades

### Produtos

- Cadastrar produtos
- Listar produtos
- Buscar produto por ID
- Validar nome, preço e estoque
- Retornar erro quando o produto não existe

### Pedidos

- Criar pedidos
- Listar pedidos
- Buscar pedido por ID
- Calcular automaticamente o valor total
- Validar disponibilidade em estoque
- Reduzir o estoque após a compra
- Impedir pedidos com quantidade inválida
- Garantir atomicidade da operação

## Regras de negócio

Ao criar um pedido, a aplicação executa o seguinte fluxo:

```text
Receber pedido
      ↓
Buscar produto
      ↓
Validar existência
      ↓
Validar estoque
      ↓
Calcular valor total
      ↓
Reduzir estoque
      ↓
Salvar pedido
      ↓
Confirmar transação
```

Se algum erro ocorrer durante a criação do pedido, a transação é desfeita e nenhuma alteração parcial permanece no banco.

## Arquitetura

O projeto utiliza uma arquitetura em camadas:

```text
Route
  ↓
Service
  ↓
Repository
  ↓
Database
```

### Routes

Responsáveis por receber as requisições HTTP, validar os dados de entrada e retornar as respostas da API.

### Services

Responsáveis pelas regras de negócio, como cálculo do valor total e validação de estoque.

### Repositories

Responsáveis pelo acesso e persistência dos dados.

### Models

Representam as tabelas e entidades persistidas pelo SQLAlchemy.

### Schemas

Definem e validam os contratos de entrada e saída da API utilizando Pydantic.

## Tecnologias

- Python
- FastAPI
- SQLAlchemy
- Pydantic
- SQLite
- Pytest
- Uvicorn
- Git

## Estrutura do projeto

```text
mini-mercado-livre/
├── app/
│   ├── core/
│   ├── database/
│   ├── dependencies/
│   ├── exceptions/
│   ├── models/
│   ├── repositories/
│   ├── routes/
│   ├── schemas/
│   ├── services/
│   └── main.py
├── tests/
│   ├── conftest.py
│   ├── test_pedido.py
│   └── test_produto.py
├── .env.example
├── .gitignore
├── requirements.txt
├── requirements-dev.txt
└── README.md
```

## Como executar

### Pré-requisitos

- Python 3.12 ou superior
- Git

### 1. Clonar o repositório

```bash
git clone URL_DO_REPOSITORIO
```

Entre na pasta:

```bash
cd Mini-mercado-livre
```

### 2. Criar o ambiente virtual

No Windows:

```powershell
python -m venv .venv
```

Ative o ambiente:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned
.\.venv\Scripts\Activate.ps1
```

Quando o ambiente estiver ativo, o terminal mostrará:

```text
(.venv)
```

### 3. Instalar as dependências

Para executar somente a aplicação:

```powershell
python -m pip install -r requirements.txt
```

Para desenvolvimento e testes:

```powershell
python -m pip install -r requirements-dev.txt
```

### 4. Configurar as variáveis de ambiente

Copie o arquivo de exemplo:

```powershell
Copy-Item .env.example .env
```

Configuração padrão:

```env
DATABASE_URL=sqlite:///mini_mercado.db
```

### 5. Iniciar a API

```powershell
python -m uvicorn app.main:app --reload
```

A API ficará disponível em:

```text
http://127.0.0.1:8000
```

## Documentação da API

Swagger:

```text
http://127.0.0.1:8000/docs
```

ReDoc:

```text
http://127.0.0.1:8000/redoc
```

## Exemplos de uso

### Criar produto

```http
POST /produtos/
```

```json
{
  "nome": "Notebook Gamer",
  "preco": 5500.00,
  "estoque": 10
}
```

Resposta esperada:

```json
{
  "id": 1,
  "nome": "Notebook Gamer",
  "preco": 5500.00,
  "estoque": 10
}
```

### Criar pedido

```http
POST /pedidos/
```

```json
{
  "produto_id": 1,
  "quantidade": 2
}
```

Resposta esperada:

```json
{
  "id": 1,
  "produto_id": 1,
  "quantidade": 2,
  "valor_total": 11000.00
}
```

Depois da criação do pedido, o estoque do produto será reduzido de `10` para `8`.

### Estoque insuficiente

Se a quantidade solicitada for maior que o estoque disponível, a API retorna:

```http
409 Conflict
```

```json
{
  "detail": "Estoque insuficiente para o produto 1. Disponível: 8. Solicitado: 100."
}
```

### Produto inexistente

```http
404 Not Found
```

```json
{
  "detail": "Produto com ID 999 não encontrado"
}
```

## Testes automatizados

Para executar os testes:

```powershell
python -m pytest -v
```

A suíte atualmente possui 20 casos de teste, incluindo:

- Cadastro de produto
- Listagem de produtos
- Busca de produto inexistente
- Validação de produtos inválidos
- Validação do contrato da API
- Criação de pedido
- Cálculo do valor total
- Redução de estoque
- Consumo total do estoque
- Quantidade zero ou negativa
- Estoque insuficiente
- Pedido para produto inexistente
- Garantia de que pedidos recusados não alteram o estoque
- Garantia de que pedidos recusados não são persistidos

Resultado esperado:

```text
20 passed
```

## Próximas evoluções

- Implementar atualização e exclusão de produtos
- Adicionar status aos pedidos
- Configurar migrations com Alembic
- Migrar o banco de SQLite para PostgreSQL
- Adicionar autenticação e autorização
- Implementar paginação e filtros
- Adicionar logs estruturados
- Adicionar observabilidade
- Implementar RabbitMQ para tarefas assíncronas
- Publicar eventos com Kafka
- Separar a aplicação em microsserviços
- Containerizar os serviços com Docker
- Configurar integração contínua

## Objetivo educacional

Este projeto foi construído de forma incremental.

A arquitetura começou simples para que novas tecnologias fossem adicionadas somente quando surgisse uma necessidade real, evitando complexidade prematura.

```text
Monolito organizado
        ↓
Regras de negócio
        ↓
Testes automatizados
        ↓
PostgreSQL
        ↓
RabbitMQ
        ↓
Kafka
        ↓
Microsserviços
```

## Autor

Desenvolvido por Enzo de Barros Francisco como projeto de estudo em desenvolvimento Back-End e arquitetura de software.
