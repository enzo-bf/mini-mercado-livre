# Mini Mercado Livre

Aplicação web de um marketplace simplificado, desenvolvida com FastAPI, SQLAlchemy, HTML, CSS e JavaScript.

O projeto permite gerenciar produtos e pedidos por meio de uma interface web integrada a uma API REST. A aplicação utiliza arquitetura em camadas, validações, controle de estoque, transações e testes automatizados.

## Tecnologias

### Back-End

- Python
- FastAPI
- SQLAlchemy
- Pydantic
- SQLite
- Uvicorn

### Front-End

- HTML5
- CSS3
- JavaScript
- Fetch API

### Testes e ferramentas

- Pytest
- Git
- GitHub
## Funcionalidades
### Iniciar o front-end

Mantenha a API em execução e abra um segundo terminal.

Entre na pasta do front-end:

```powershell
cd frontend

### Produtos

- Cadastrar produtos
- Listar produtos
- Buscar produto por ID
- Atualizar produto por ID
- Excluir produto por ID quando não houver pedidos associados
- Validar nome, preço e estoque
- Retornar erro quando o produto não existe
- Retornar conflito ao excluir produto associado a pedido

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
git clone https://github.com/enzo-bf/mini-mercado-livre.git
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

### Atualizar produto

```http
PUT /produtos/1
```

```json
{
  "nome": "Notebook Profissional",
  "preco": 6200.00,
  "estoque": 15
}
```

O PUT exige os três campos do produto e substitui os valores atuais.

### Excluir produto

```http
DELETE /produtos/1
```

A API retorna `204 No Content` quando a exclusão é realizada. Produtos associados a
pedidos não podem ser excluídos e retornam `409 Conflict`.

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

A suíte atualmente possui 27 casos de teste, incluindo:

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
- Atualização de produto
- Exclusão de produto
- Bloqueio de exclusão de produto associado a pedido
- Busca de pedido inexistente

Resultado esperado:

```text
20 passed
```


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
### Interface web

- Dashboard com resumo de produtos, pedidos e estoque
- Cadastro de produtos
- Edição de produtos
- Exclusão de produtos
- Criação de pedidos
- Listagem do histórico de pedidos
- Atualização automática do estoque
- Exibição de mensagens de sucesso e erro
- Layout responsivo
- Integração com a API utilizando Fetch API


## Autor

Desenvolvido por Enzo de Barros Francisco como projeto de estudo em desenvolvimento Back-End e arquitetura de software.
