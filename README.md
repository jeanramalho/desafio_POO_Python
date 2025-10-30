# Desafio: Sistema Bancário Orientado a Objetos (UML)

**Autor:** Jean Ramalho  
**Tipo:** Exercício / Refatoração (POO)  
**Linguagem:** Python 3.x

---

## Visão geral

Neste desafio atualizamos a implementação do sistema bancário para armazenar clientes e contas como objetos (instâncias de classes) seguindo o modelo de classes definido em UML. O objetivo é trabalhar com encapsulamento, responsabilidade por comportamento (métodos) e histórico de transações, mantendo a interface de linha de comando (CLI) para interação.

O repositório contém uma implementação simples, legível e orientada a objetos que serve como base para extensões e testes.

---

## Objetivo do desafio

- Substituir estruturas baseadas em dicionários por classes com estados e comportamentos.
- Seguir o modelo de classes UML (Cliente, PessoaFisica, Conta, ContaCorrente, Historico, Transacao, Saque, Deposito).
- Preservar o fluxo interativo via CLI.
- Garantir código claro, conciso e documentado de forma profissional.

---

## Funcionalidades

- Criar cliente (Pessoa Física) via CLI.
- Criar conta corrente vinculada ao cliente.
- Depositar valores em conta.
- Sacar valores (com limite por saque e limite no número de saques).
- Registrar histórico de transações com timestamp.
- Exibir extrato e saldo.
- Listar contas existentes.
- Loop interativo com menu de opções.

---

## Estrutura do projeto

```
.
├── desafio.py        # Implementação principal (classes e CLI)
└── README.md         # Este documento
```

Principais classes implementadas (conforme UML):

- `Cliente` — entidade base que mantém endereço e lista de contas.
- `PessoaFisica(Cliente)` — cliente com nome, data de nascimento e CPF.
- `Conta` — conta bancária básica com saldo, número, agência e histórico.
- `ContaCorrente(Conta)` — conta com regras de limite por saque e número máximo de saques.
- `Historico` — armazena transações em memória (lista).
- `Transacao` (abstrata) — contrato das transações (propriedade `valor`, método `registrar`).
- `Saque(Transacao)` e `Deposito(Transacao)` — implementações concretas que delegam execução para `Conta` e registram no `Historico`.

---

## Requisitos

- Python 3.8+ (testado com Python 3.10+)
- Nenhuma dependência externa

---

## Execução

Abra um terminal na pasta do projeto e execute:

```bash
python3 desafio.py
```

O programa inicia o loop interativo e apresenta o menu com as opções:

- `nu` — Novo usuário
- `nc` — Nova conta
- `d`  — Depositar
- `s`  — Sacar
- `e`  — Extrato
- `lc` — Listar contas
- `q`  — Sair

Os prompts são exibidos em português.

---

## Exemplos de uso (fluxo CLI)

1. `nu` → informar CPF, nome, data de nascimento e endereço  
2. `nc` → informar CPF do cliente para vincular a nova conta  
3. `d`  → informar CPF e valor do depósito (positivo)  
4. `s`  → informar CPF e valor do saque (respeitando limites)  
5. `e`  → visualizar extrato e saldo  

---

## Contratos e comportamento das principais entidades

### `Cliente.realizar_transacao(conta, transacao)`
- **Entrada:** instância de `Conta`, instância de `Transacao`.
- **Comportamento:** chama `transacao.registrar(conta)`; não altera diretamente o estado da conta.

### `Conta.sacar(valor)` / `Conta.depositar(valor)`
- **Entrada:** `valor` (float)
- **Saída:** `True` se operação bem-sucedida, `False` caso contrário.
- **Comportamento:** validações locais (saldo, valor positivo). Atualiza `_saldo` quando apropriado e imprime feedback ao usuário.

### `ContaCorrente.sacar(valor)`
- **Entrada:** `valor` (float)
- **Comportamento:** verifica limite por saque e número máximo de saques (contabilizados pelo `Historico`) e, se válido, delega para `Conta.sacar`.

### `Historico.adicionar_transacao(transacao)`
- **Entrada:** instância de `Transacao`
- **Comportamento:** armazena dicionário com `tipo`, `valor` e `data` (timestamp formatado).

### `Transacao.registrar(conta)`
- **Entrada:** instância de `Conta`
- **Comportamento:** executa operação (`sacar` ou `depositar`) e registra no histórico em caso de sucesso.

---

## Validações e comportamentos de borda

- Depósitos com `valor <= 0` são rejeitados.
- Saques com `valor <= 0` são rejeitados.
- Saques que excedem o saldo são rejeitados.
- Saques acima do limite por operação são rejeitados.
- Quando o cliente não possui conta, operações que dependem de conta exibem mensagem e abortam.
- A seleção de conta do cliente retorna a primeira conta associada (não há escolha entre múltiplas contas no CLI).

---

## Observações técnicas

- O `Historico` guarda timestamps com `datetime.now().strftime("%d-%m-%Y %H:%M:%s")`.
- As mensagens e feedback ao usuário são exibidos via `print` no CLI.
- O projeto é concebido para ser didático; decisões de simplicidade foram deliberadas (persistência em memória, IO direto, validação mínima).

---

## Possíveis melhorias (não implementadas neste desafio)

- Persistência em arquivo (JSON/SQLite) para manter dados entre execuções.
- Separar lógica de negócio da camada de IO (facilita testes).
- Substituir prints por `logging` configurável.
- Tornar o contador de saques persistente por período (ex.: por dia).
- Converter `data_nascimento` para `datetime.date` com validação de formato.
- Adicionar testes unitários (pytest) cobrindo regras de negócio.

---

## Contribuição

Fork e pull requests são bem-vindos. Abra issues para relatar bugs ou sugerir melhorias.

---

## Licença

Este projeto está sob a licença MIT.

---
