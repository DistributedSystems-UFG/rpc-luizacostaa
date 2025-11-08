# Sistema Cliente-Servidor para Manipulação de Vetor (RPyC)

Este projeto implementa um sistema simples de **cliente-servidor** utilizando `RPyC` (Remote Python Call), permitindo que o cliente envie comandos para manipular um vetor armazenado no servidor.  
É um exercício de programação distribuída focado em comunicação remota, chamadas expostas e tratamento de erros.

---

## Tecnologias utilizadas

- **Python 3**
- **RPyC** (Remote Python Call)
- Comunicação via **TCP**
- Execução do servidor e cliente em terminais separados

---

## Funcionalidades implementadas

O servidor mantém um vetor (lista) e o cliente envia operações para manipular esse vetor.  
As operações disponíveis são:

### 🔹 Exibir lista  
Mostra o conteúdo atual do vetor. Realizada pela função exposed_show

### 🔹 Inserir número no final  
Adiciona um elemento ao final da lista. Realizada pela função exposed_append

### 🔹 Inserir número em posição específica  
Permite escolher a posição e o valor a ser inserido. Realizada pela função exposed_insert

### 🔹 Limpar a lista  
Remove todos os elementos do vetor. Realizada pela função exposed_clear

### 🔹 Remover elemento em posição específica  
Remove o item da posição informada pelo usuário. Realizada pela função exposed_remove

### 🔹 Buscar valor  
Retorna a posição onde o valor aparece (ou uma mensagem de não encontrado). Realizada pela função exposed_search

### 🔹 Ordenar vetor  
Ordena o vetor de forma crescente no servidor. Realizada pela função exposed_sort

### 🔹 Encerrar  
Fecha o cliente (e opcionalmente o servidor, dependendo da implementação). Realizada pela função on_disconnect

---

## Como executar

### Instale as dependências

```bash
pip install rpyc

```

### Inicie o servidor
```bash
python server.py

```

### Inicie o cliente
```bash
python client.py

```

### Escolha o número da operação que deseja executar
=== MENU DE OPERAÇÕES ===

1 - Mostrar lista

2 - Inserir número no final

3 - Inserir número em posição específica

4 - Limpar lista

5 - Sair

6 - Remover número em uma posição específica

7 - Buscar elemento

8 - Ordenar lista

## Observações sobre o desenvolvimento do trabalho
- IMplementei cada operação aos poucos
- Implementei a função de append, mas logo percebi a necessidade de implementar logs de conexão 
	- on_connect: serviu para mostrar em que momento o cliente se conectou
	- on_disconnect: serviu para mostrar o momento de desconexão feito pelo cliente
	- exposed_ping: serviu para conferir se o servidor ainda estava conectado. Apliquei essa função em vários momentos para que o usuário não completasse uma operação para logo descobrir que ela não é mais válida por falta de conexão com o servidor
- Usei a função exposed_show para mostrar a lista em funções que tem a remoção, adição ou atualização do vetor. A reutilização dessa função dentro de outas funções serviu para estudo de funções que chamam outras. Um exemplo de log causado por essa reutilização é:
	[SERVER] 22:36:33 - insert()
	[SERVER] 22:36:33 - show()

- Fiz tratamento das entradas que o usuário pode fazer
- O RPyC ajudou bastante por ter funções já implementadas. Ele gera stubs automaticamente. Ele também permitiu que um processo chamasse funções de outro processo de forma remota via RPC.

- Para impedir que qualquer erro vindo do servidor quebre o cliente, eu criei o safe_call, que é tipo um protetor de chamadas remotas. Porque, se, por exemplo, o cliente chamar uma função no servidor, porém se o servidor cair, fechar ou der erro, um feedback mais intuitivo será retornado ao cliente.

	
	