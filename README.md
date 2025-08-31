# Sistema de Controle Financeiro

Este projeto oferece uma solução simples para o gerenciamento de transações financeiras, com funcionalidades para adicionar, listar, remover transações e calcular o saldo. A aplicação foi construída utilizando o Python com Flask, e a persistência de dados é realizada por meio de arquivos JSON.

## Repositório no GitHub

Você pode encontrar o código-fonte completo deste projeto no repositório do GitHub:

[https://github.com/Mabynha20/Teste-de-Software-de-Transa-es-Financeiras.git]

### Como Usar o Projeto a Partir do GitHub

1. **Clonar o Repositório**
   - Para começar a usar o projeto, você precisa clonar o repositório em sua máquina local. No terminal, execute o seguinte comando:

   ```bash
   git clone https://github.com/Mabynha20/Teste-de-Software-de-Transa-es-Financeiras.git
   ```

2. **Acessar o Diretório do Projeto**
   - Após clonar o repositório, navegue até o diretório do projeto:

   ```bash
   cd Teste-de-Software-de-Transa-es-Financeiras
   ```

3. **Instalar as Dependências**
   - Certifique-se de que você tem o Python 3.x instalado em sua máquina. Depois, instale as dependências necessárias:

   ```bash
   pip install flask
   ```

4. **Executar a API**
   - Para rodar a API Flask localmente, você pode usar os seguintes comandos:

   ```bash
   export FLASK_APP=src/api/routes.py
   export FLASK_ENV=development
   flask run
   ```

   A API estará disponível em `http://127.0.0.1:5000`.

5. **Executar o Menu de Linha de Comando**
   - Para interagir com o sistema via terminal, você pode rodar o menu de linha de comando com:

   ```bash
   python src/main.py
   ```

## Estrutura do Projeto

O projeto é composto pelas seguintes partes principais:

- **FinanceManager**: Responsável pela gestão das transações financeiras, incluindo operações de adição, listagem, remoção e cálculo do saldo.
- **Transaction**: Representa uma transação financeira, com atributos como tipo (entrada ou saída), descrição, valor e data.
- **API Flask**: Interface HTTP para interação com o sistema de controle financeiro. As rotas implementadas incluem criação, listagem, atualização e remoção de transações, além da visualização do saldo.
- **Menu**: Interface de linha de comando para interagir com o sistema de controle financeiro diretamente no terminal.

## Funcionalidades

### **FinanceManager**

A classe `FinanceManager` oferece as seguintes funcionalidades para manipulação das transações:

#### 1. Adicionar Transação

Método `adicionar_transacao(tipo: str, descricao: str, valor: float) -> Transaction`

Adiciona uma nova transação ao sistema. A transação pode ser de tipo "entrada" ou "saida". O valor da transação é especificado em reais.

#### 2. Listar Transações

Método `listar_transacoes() -> List[Transaction]`

Retorna uma lista de todas as transações registradas, contendo informações como tipo, descrição, valor e data.

#### 3. Remover Transação

Método `remover_transacao(tid: int) -> bool`

Remove uma transação pelo seu ID. Retorna `True` se a transação for removida com sucesso, e `False` caso a transação não exista.

#### 4. Calcular Saldo

Método `calcular_saldo() -> float`

Calcula e retorna o saldo atual com base nas transações registradas. O saldo é a soma das entradas menos as saídas.

#### 5. Atualizar Transação

Método `atualizar_transacao(tid: int, tipo: Optional[str] = None, descricao: Optional[str] = None, valor: Optional[float] = None) -> Optional[Transaction]`

Atualiza os dados de uma transação existente. Pode-se atualizar o tipo, a descrição e o valor da transação. Retorna a transação atualizada ou `None` caso a transação não seja encontrada.

### **Transaction**

A classe `Transaction` representa uma transação financeira e contém os seguintes atributos:

- `id`: Identificador único da transação.
- `tipo`: Tipo da transação, que pode ser "entrada" ou "saida".
- `descricao`: Descrição da transação.
- `valor`: Valor da transação.
- `data`: Data e hora da transação, no formato `YYYY-MM-DD HH:MM:SS`.

#### Métodos:
- `to_dict()`: Converte a transação para um dicionário, para fácil conversão em JSON.
- `from_dict(d: dict)`: Converte um dicionário para uma instância de `Transaction`.

### **API Flask**

A API oferece as seguintes rotas:

#### 1. `GET /transactions`

Retorna uma lista de todas as transações registradas.

#### 2. `POST /transactions`

Cria uma nova transação com os dados fornecidos no corpo da requisição (tipo, descrição, valor).

#### 3. `DELETE /transactions/<int:tid>`

Remove uma transação pelo seu ID.

#### 4. `GET /balance`

Retorna o saldo atual, calculado com base nas transações.

#### 5. `PUT /transactions/<int:tid>`

Atualiza uma transação existente, alterando seu tipo, descrição ou valor.

### **Menu de Linha de Comando**

O menu de linha de comando oferece uma interface para interagir com o sistema. As opções são:

1. **Adicionar entrada**: Adiciona uma transação do tipo "entrada".
2. **Adicionar saída**: Adiciona uma transação do tipo "saida".
3. **Listar transações**: Exibe todas as transações registradas.
4. **Ver saldo**: Exibe o saldo atual.
5. **Remover transação**: Remove uma transação pelo seu ID.
6. **Sair**: Encerra o menu.

## Requisições para Testar a API no Postman

Para testar a API do projeto utilizando o **Postman**, você pode seguir as instruções abaixo para realizar as requisições.

### **1. Listar Transações**  
- **Método**: `GET`
- **URL**: `http://127.0.0.1:5000/transactions`
- **Descrição**: Retorna a lista de todas as transações registradas.
- **Resposta Esperada**:

```json
[
    {
        "id": 1,
        "tipo": "entrada",
        "descricao": "Compra de alimentos",
        "valor": 100.0,
        "data": "2025-30-08 20:21:15"
    },
    {
        "id": 2,
        "tipo": "saida",
        "descricao": "Pagamento de contas",
        "valor": 50.0,
        "data": "2025-30-08 20:22:30"
    }
]
```

### **2. Criar uma Transação (Entrada ou Saída)**  
- **Método**: `POST`
- **URL**: `http://127.0.0.1:5000/transactions`
- **Descrição**: Cria uma nova transação (entrada ou saída).
- **Body**: 
```json
{
    "tipo": "entrada",
    "descricao": "Venda de produto",
    "valor": 200.0
}
```
- **Resposta Esperada**:

```json
{
    "id": 3,
    "tipo": "entrada",
    "descricao": "Venda de produto",
    "valor": 200.0,
    "data": "2025-30-08 20:25:10"
}
```

### **3. Remover uma Transação**  
- **Método**: `DELETE`
- **URL**: `http://127.0.0.1:5000/transactions/{id}`
- **Descrição**: Remove a transação com o ID fornecido.
- **Exemplo**: Para remover a transação com ID `3`, a URL seria `http://127.0.0.1:5000/transactions/3`
- **Resposta Esperada**:

```json
{
    "ok": true
}
```

- **Se a transação não for encontrada**:

```json
{
    "error": "Transação não encontrada"
}
```

### **4. Consultar o Saldo Atual**  
- **Método**: `GET`
- **URL**: `http://127.0.0.1:5000/balance`
- **Descrição**: Retorna o saldo atual calculado com base nas transações (entradas e saídas).
- **Resposta Esperada**:

```json
{
    "balance": 250.0
}
```

### **5. Atualizar uma Transação**  
- **Método**: `PUT`
- **URL**: `http://127.0.0.1:5000/transactions/{id}`
- **Descrição**: Atualiza a transação com o ID fornecido.
- **Body**:
```json
{
    "tipo": "saida",
    "descricao": "Pagamento de serviços",
    "valor": 75.0
}
```
- **Exemplo**: Para atualizar a transação com ID `2`, a URL seria `http://127.0.0.1:5000/transactions/2`
- **Resposta Esperada**:

```json
{
    "id": 2,
    "tipo": "saida",
    "descricao": "Pagamento de serviços",
    "valor": 75.0,
    "data": "2025-30-08 20:28:40"
}
```

- **Se a transação não for encontrada**:

```json
{
    "error": "Transação não encontrada"
}
```

### **6. Erro ao Criar Transação (Campos Ausentes)**  
- **Método**: `POST`
- **URL**: `http://127.0.0.1:5000/transactions`
- **Body**:  
```json
{
    "descricao": "Compra de equipamento",
    "valor": 150.0
}
```
- **Resposta Esperada**:

```json
{
    "error": "Campos obrigatórios ausentes: tipo"
}
```

### **7. Erro ao Criar Transação (Valor Não Numérico)**  
- **Método**: `POST`
- **URL**: `http://127.0.0.1:5000/transactions`
- **Body**:  
```json
{
    "tipo": "entrada",
    "descricao": "Venda de item",
    "valor": "cento"
}
```
- **Resposta Esperada**:

```json
{
    "error": "Valor deve ser numérico"
}
```

### **8. Erro ao Criar Transação (Tipo Inválido)**  
- **Método**: `POST`
- **URL**: `http://127.0.0.1:5000/transactions`
- **Body**:  
```json
{
    "tipo": "investimento",
    "descricao": "Investimento em ação",
    "valor": 1000.0
}
```
- **Resposta Esperada**:

```json
{
    "error": "Tipo deve ser 'entrada' ou 'saida'"
}
```#   T e s t e - d e - S o f t w a r e - d e - T r a n s a - e s - F i n a n c e i r a s  
 #   T e s t e - d e - S o f t w a r e - d e - T r a n s a - e s - F i n a n c e i r a s  
 #   T e s t e - d e - S o f t w a r e - d e - T r a n s a - e s - F i n a n c e i r a s  
 