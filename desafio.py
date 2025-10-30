import textwrap
from abc import ABC, abstractclassmethod, abstractproperty
from datetime import datetime

# Módulo: desafio.py
# Objetivo: exercício de Programação Orientada a Objetos (POO) que simula operações
# bancárias básicas (criação de clientes/contas, depósito, saque e extrato).
#
# Observação de estilo: adicionei comentários explicativos para cada classe e
# função sem alterar a lógica. Os comentários seguem um tom profissional e
# objetivo, como se escritos por um desenvolvedor experiente no projeto.


class Cliente:
    def __init__(self, endereco):
        self.endereco = endereco
        self.contas = []

    def realizar_transacao(self, conta, transacao):
        # Delegação explícita: a responsabilidade de executar a operação é da
        # Transacao (Saque/Deposito) e da Conta. O Cliente apenas orquestra a
        # chamada — isso mantém boa separação de responsabilidades.
        transacao.registrar(conta)

    def adicionar_conta(self, conta):
        self.contas.append(conta)


class PessoaFisica(Cliente):
    def __init__(self, nome, data_nascimento, cpf, endereco):
        super().__init__(endereco)
        self.nome = nome
        self.data_nascimento = data_nascimento
        self.cpf = cpf

# Nota: data_nascimento é armazenada como string neste exercício. Em um
# cenário real eu preferiria armazenar como datetime.date para permitir validação
# e cálculos (idade, vencimento de documentos, etc.).


class Conta:
    def __init__(self, numero, cliente):
        self._saldo = 0
        self._numero = numero
        self._agencia = "0001"
        self._cliente = cliente
        self._historico = Historico()

    @classmethod
    def nova_conta(cls, cliente, numero):
        return cls(numero, cliente)

    @property
    def saldo(self):
        return self._saldo

    @property
    def numero(self):
        return self._numero

    @property
    def agencia(self):
        return self._agencia

    @property
    def cliente(self):
        return self._cliente

    @property
    def historico(self):
        return self._historico

    def sacar(self, valor):
        saldo = self.saldo
        excedeu_saldo = valor > saldo

        # Fluxo de validação simples: primeiro verificamos saldo suficiente,
        # depois validade do valor. Mantemos retornos booleanos e prints para a
        # interface CLI existente. Em código de produção considerar exceptions
        # para erros e separar mensagens da lógica.
        if excedeu_saldo:
            print("\n@@@ Operação falhou! Você não tem saldo suficiente. @@@")

        elif valor > 0:
            # Atualiza o estado interno do saldo apenas quando válido
            self._saldo -= valor
            print("\n=== Saque realizado com sucesso! ===")
            return True

        else:
            print("\n@@@ Operação falhou! O valor informado é inválido. @@@")

        return False

    def depositar(self, valor):
        # Validação do valor do depósito. Retornamos booleano indicando sucesso
        # para manter compatibilidade com a lógica que registra transações.
        if valor > 0:
            self._saldo += valor
            print("\n=== Depósito realizado com sucesso! ===")
        else:
            print("\n@@@ Operação falhou! O valor informado é inválido. @@@")
            return False

        return True


class ContaCorrente(Conta):
    def __init__(self, numero, cliente, limite=500, limite_saques=3):
        super().__init__(numero, cliente)
        self._limite = limite
        self._limite_saques = limite_saques

    def sacar(self, valor):
        numero_saques = len(
            [transacao for transacao in self.historico.transacoes if transacao["tipo"] == Saque.__name__]
        )

        excedeu_limite = valor > self._limite
        excedeu_saques = numero_saques >= self._limite_saques

        # Conta corrent com regras extras: limite por saque e limite no número de
        # saques. Aqui contamos os saques já realizados no histórico da conta.
        # Observação: o limite de número de saques é global desde a criação da
        # conta — se a intenção for limitar por período (ex.: diário), seria
        # preciso filtrar por timestamp das transações.
        if excedeu_limite:
            print("\n@@@ Operação falhou! O valor do saque excede o limite. @@@")

        elif excedeu_saques:
            print("\n@@@ Operação falhou! Número máximo de saques excedido. @@@")

        else:
            return super().sacar(valor)

        return False

    def __str__(self):
        return f"""\
            Agência:\t{self.agencia}
            C/C:\t\t{self.numero}
            Titular:\t{self.cliente.nome}
        """


class Historico:
    def __init__(self):
        self._transacoes = []

    @property
    def transacoes(self):
        return self._transacoes

    def adicionar_transacao(self, transacao):
        # Registra um dicionário com tipo, valor e carimbo de data/hora.
        # Observação importante: o formato de segundos correto é '%S' (maiúsculo).
        # Aqui mantive o formato original do exercício, mas em revisões futuras
        # recomendo trocar '%s' por '%S' para evitar inconsistências entre
        # plataformas/implementações do strftime.
        self._transacoes.append(
            {
                "tipo": transacao.__class__.__name__,
                "valor": transacao.valor,
                "data": datetime.now().strftime("%d-%m-%Y %H:%M:%s"),
            }
        )


class Transacao(ABC):
    @property
    @abstractproperty
    def valor(self):
        pass

    @abstractclassmethod
    def registrar(self, conta):
        pass

# Nota sobre classes abstratas: este padrão usa `abstractproperty` e
# `abstractclassmethod`. Hoje em dia é comum usar `@property` +
# `@abstractmethod` para propriedades abstratas e `@abstractmethod` para
# métodos de instância — a implementação atual funciona para o exercício,
# mas vale considerar a modernização para maior clareza.


class Saque(Transacao):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor

    def registrar(self, conta):
        sucesso_transacao = conta.sacar(self.valor)

        # Se a conta aceitar o saque, registramos no histórico.
        if sucesso_transacao:
            conta.historico.adicionar_transacao(self)


class Deposito(Transacao):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor

    def registrar(self, conta):
        sucesso_transacao = conta.depositar(self.valor)

        # Análogo ao Saque: ao depositar com sucesso adicionamos ao histórico.
        if sucesso_transacao:
            conta.historico.adicionar_transacao(self)


def menu():
    menu = """\n
    ================ MENU ================
    [d]\tDepositar
    [s]\tSacar
    [e]\tExtrato
    [nc]\tNova conta
    [lc]\tListar contas
    [nu]\tNovo usuário
    [q]\tSair
    => """
    return input(textwrap.dedent(menu))

# Interface de console: função simples que retorna a opção escolhida pelo
# usuário. Mantida intencionalmente simples para o escopo do exercício.


def filtrar_cliente(cpf, clientes):
    clientes_filtrados = [cliente for cliente in clientes if cliente.cpf == cpf]
    return clientes_filtrados[0] if clientes_filtrados else None

# Busca linear por CPF — suficiente para conjuntos pequenos usados em
# exercícios. Em aplicações reais usar estrutura indexada (dict) ou banco.


def recuperar_conta_cliente(cliente):
    if not cliente.contas:
        print("\n@@@ Cliente não possui conta! @@@")
        return

    # FIXME: não permite cliente escolher a conta
    return cliente.contas[0]

# Atenção: aqui sempre retornamos a primeira conta do cliente. Se o cliente
# tiver múltiplas contas, o usuário não conseguirá escolher; o FIXME no código
# já indica esse ponto.


def depositar(clientes):
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print("\n@@@ Cliente não encontrado! @@@")
        return

    valor = float(input("Informe o valor do depósito: "))
    transacao = Deposito(valor)

    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return

    cliente.realizar_transacao(conta, transacao)

# Observação de UX: as conversões `float(input(...))` podem levantar
# ValueError se o usuário digitar texto inválido. Em produção envolveria
# validação/loop de reentrada.


def sacar(clientes):
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print("\n@@@ Cliente não encontrado! @@@")
        return

    valor = float(input("Informe o valor do saque: "))
    transacao = Saque(valor)

    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return

    cliente.realizar_transacao(conta, transacao)


def exibir_extrato(clientes):
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print("\n@@@ Cliente não encontrado! @@@")
        return

    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return

    print("\n================ EXTRATO ================")
    transacoes = conta.historico.transacoes

    extrato = ""
    if not transacoes:
        extrato = "Não foram realizadas movimentações."
    else:
        for transacao in transacoes:
            extrato += f"\n{transacao['tipo']}:\n\tR$ {transacao['valor']:.2f}"

    print(extrato)
    print(f"\nSaldo:\n\tR$ {conta.saldo:.2f}")
    print("==========================================")

# A apresentação do extrato é básica e clara. Para melhorar: incluir datas e
# formatar cada transação com timestamp (já gravado no histórico).


def criar_cliente(clientes):
    cpf = input("Informe o CPF (somente número): ")
    cliente = filtrar_cliente(cpf, clientes)

    if cliente:
        print("\n@@@ Já existe cliente com esse CPF! @@@")
        return

    nome = input("Informe o nome completo: ")
    data_nascimento = input("Informe a data de nascimento (dd-mm-aaaa): ")
    endereco = input("Informe o endereço (logradouro, nro - bairro - cidade/sigla estado): ")

    cliente = PessoaFisica(nome=nome, data_nascimento=data_nascimento, cpf=cpf, endereco=endereco)

    clientes.append(cliente)

    print("\n=== Cliente criado com sucesso! ===")

# Criação simples de cliente com checagem de CPF já existente feita na função
# que chama esta rotina. Em código real, considerar validação do formato do CPF.


def criar_conta(numero_conta, clientes, contas):
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print("\n@@@ Cliente não encontrado, fluxo de criação de conta encerrado! @@@")
        return

    conta = ContaCorrente.nova_conta(cliente=cliente, numero=numero_conta)
    contas.append(conta)
    cliente.contas.append(conta)

    print("\n=== Conta criada com sucesso! ===")

# A numeração de contas é incremental com base em `len(contas)`; para testes
# e exercícios isso é suficiente, mas em produção usar gerador sequencial
# persistente para evitar colisões.


def listar_contas(contas):
    for conta in contas:
        print("=" * 100)
        print(textwrap.dedent(str(conta)))

# Impressão formatada das contas — boa separação: a própria Conta define seu
# formato via `__str__` e a listagem apenas exibe.


def main():
    clientes = []
    contas = []

    while True:
        opcao = menu()

        if opcao == "d":
            depositar(clientes)

        elif opcao == "s":
            sacar(clientes)

        elif opcao == "e":
            exibir_extrato(clientes)

        elif opcao == "nu":
            criar_cliente(clientes)

        elif opcao == "nc":
            numero_conta = len(contas) + 1
            criar_conta(numero_conta, clientes, contas)

        elif opcao == "lc":
            listar_contas(contas)

        elif opcao == "q":
            break

        else:
            print("\n@@@ Operação inválida, por favor selecione novamente a operação desejada. @@@")


main()

# Ponto final: `main()` roda a aplicação em modo interativo. Para tornar o
# módulo testável seria interessante proteger a execução com
# `if __name__ == "__main__": main()` — assim evita side-effects ao importar
# o módulo em testes automatizados.