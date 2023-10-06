import pandas as pd
import os

# Verificar se o arquivo 'cashback.xlsx' existe; se não, criar um DataFrame vazio com as colunas desejadas
if not os.path.exists('cashback.xlsx'):
    df = pd.DataFrame(columns=['CPF', 'Nome', 'Cidade', 'Cashback'])
    df.to_excel('cashback.xlsx', index=False)


def calcular_cashback(valor):
    return valor * 0.02


def validar_cpf(cpf):
    # Remover qualquer caractere não numérico
    cpf = ''.join(filter(str.isdigit, cpf))

    if len(cpf) == 11:
        return cpf
    else:
        raise ValueError("CPF deve ter 11 dígitos.")


def cpf_ja_cadastrado(cpf):
    try:
        # Carregar a planilha Excel
        df = pd.read_excel('cashback.xlsx')

        # Verificar se o CPF já está na lista de clientes
        return cpf in df['CPF'].values

    except FileNotFoundError:
        return False


def cadastrar_cliente(clientes, cliente_info):
    try:
        # Validar o CPF
        cpf = validar_cpf(cliente_info['CPF'])

        # Verificar se o CPF já existe na planilha
        if cpf_ja_cadastrado(cpf):
            raise ValueError("CPF já cadastrado.")

        # Adicionar o novo cliente à lista com o cashback calculado
        cliente_info['CPF'] = cpf  # Atualiza o CPF validado
        cliente_info['Cashback'] = calcular_cashback(cliente_info['Valor'])

        # Carregar a planilha Excel
        df = pd.read_excel('cashback.xlsx')

        # Criar um novo DataFrame com o novo cliente
        novo_cliente_df = pd.DataFrame([cliente_info])

        # Concatenar o novo DataFrame com o DataFrame existente
        df = pd.concat([df, novo_cliente_df], ignore_index=True)

        # Salvar o DataFrame no arquivo Excel
        df.to_excel('cashback.xlsx', index=False)

        # Imprimir a mensagem de sucesso com o valor do cashback
        print(f"Cliente cadastrado com sucesso! Valor do cashback: R${
              cliente_info['Cashback']:.2f}")

    except Exception as e:
        print(f"Erro ao cadastrar o cliente: {str(e)}")


def consultar_saldo(clientes, cpf):
    try:
        # Validar o CPF
        cpf = validar_cpf(cpf)

        # Carregar a planilha Excel
        df = pd.read_excel('cashback.xlsx')

        # Procurar pelo cliente com o CPF especificado
        cliente = df[df['CPF'] == cpf]
        if not cliente.empty:
            saldo_atual = cliente.iloc[0]['Cashback']
            nome_cliente = cliente.iloc[0]['Nome']

            print(f"Nome do cliente: {nome_cliente}")
            print(f"Saldo de Cashback atual: R${saldo_atual:.2f}")

            utilizar_saldo = input(
                "Deseja utilizar o saldo? (S/N): ").strip().lower()
            if utilizar_saldo == 's':
                valor_utilizado = float(
                    input("Digite o valor a ser utilizado: "))
                if valor_utilizado <= saldo_atual:
                    saldo_novo = saldo_atual - valor_utilizado
                    df.loc[df['CPF'] == cpf, 'Cashback'] = saldo_novo
                    df.to_excel('cashback.xlsx', index=False)
                    print(f"Saldo utilizado com sucesso! Novo saldo: R${
                          saldo_novo:.2f}")
                else:
                    print("Saldo insuficiente para a transação.")
            else:
                return

        else:
            print("Cliente não encontrado.")
    except FileNotFoundError:
        print("A planilha 'cashback.xlsx' ainda não foi criada.")


def adicionar_compra(clientes, cpf, valor_compra):
    try:
        # Carregar a planilha Excel
        df = pd.read_excel('cashback.xlsx')

        # Procurar pelo cliente com o CPF especificado
        cliente = df[df['CPF'] == cpf]
        if not cliente.empty:
            saldo_atual = cliente.iloc[0]['Cashback']
            nome_cliente = cliente.iloc[0]['Nome']

            # Calcular o cashback da compra
            cashback = calcular_cashback(valor_compra)

            # Atualizar o saldo de cashback na planilha
            novo_saldo = saldo_atual + cashback
            df.loc[df['CPF'] == cpf, 'Cashback'] = novo_saldo
            df.to_excel('cashback.xlsx', index=False)

            print(f"Cliente: {nome_cliente}")
            print(f"Saldo antigo: R${saldo_atual:.2f}")
            print(f"Saldo novo: R${novo_saldo:.2f}")
        else:
            print("Cliente não encontrado.")
    except FileNotFoundError:
        print("A planilha 'cashback.xlsx' ainda não foi criada.")


def utilizar_saldo(clientes, cpf, valor_utilizado):
    try:
        # Carregar a planilha Excel
        df = pd.read_excel('cashback.xlsx')

        # Procurar pelo cliente com o CPF especificado
        cliente = df[df['CPF'] == cpf]
        if not cliente.empty:
            saldo_atual = cliente.iloc[0]['Cashback']
            nome_cliente = cliente.iloc[0]['Nome']

            if valor_utilizado <= saldo_atual:
                saldo_novo = saldo_atual - valor_utilizado
                df.loc[df['CPF'] == cpf, 'Cashback'] = saldo_novo
                df.to_excel('cashback.xlsx', index=False)

                print(f"Cliente: {nome_cliente}")
                print(f"Saldo antigo: R${saldo_atual:.2f}")
                print(f"Saldo novo: R${saldo_novo:.2f}")
            else:
                print("Saldo insuficiente para a transação.")
        else:
            print("Cliente não encontrado.")
    except FileNotFoundError:
        print("A planilha 'cashback.xlsx' ainda não foi criada.")


def main():
    try:
        # Tentar carregar clientes existentes do arquivo Excel
        df = pd.read_excel('cashback.xlsx')
        clientes = df.to_dict('records')
    except FileNotFoundError:
        clientes = []

    while True:
        print("\nSistema de Cashback")
        print("1 - Cadastrar Cliente")
        print("2 - Consultar Saldo")
        print("3 - Adicionar Compra")
        print("4 - Utilizar Saldo")
        print("5 - Sair")

        opcao = input("Escolha uma opção: ").strip()

        if opcao == '1':
            cliente_info = {}
            cliente_info['CPF'] = input(
                "Digite o CPF do cliente (11 dígitos, sem pontos): ")
            cliente_info['Nome'] = input("Digite o nome do cliente: ")
            cliente_info['Cidade'] = input(
                "Digite a cidade do cliente: ")  # Adicionar campo cidade
            cliente_info['Valor'] = float(input("Digite o valor da compra: "))
            cadastrar_cliente(clientes, cliente_info)
        elif opcao == '2':
            cpf = input("Digite o CPF do cliente: ")
            consultar_saldo(clientes, cpf)
        elif opcao == '3':
            cpf = input("Digite o CPF do cliente: ")
            valor_compra = float(input("Digite o valor da compra: "))
            adicionar_compra(clientes, cpf, valor_compra)
        elif opcao == '4':
            cpf = input("Digite o CPF do cliente: ")
            valor_utilizado = float(input("Digite o valor a ser utilizado: "))
            utilizar_saldo(clientes, cpf, valor_utilizado)
        elif opcao == '5':
            print("Saindo do programa...")
            break
        else:
            print("Opção inválida. Tente novamente.")


if __name__ == "__main__":
    main()
