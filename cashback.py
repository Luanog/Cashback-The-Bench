import csv


def cadastrar_cliente():
    cpf = input("Digite o CPF do cliente: ")
    nome = input("Digite o nome do cliente: ")
    cidade = input("Digite a cidade do cliente: ")

    # Verifica se o CPF já está cadastrado
    with open('cashback.csv', 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            if cpf == row[0]:
                print("CPF já cadastrado. Por favor, tente novamente.")
                return

    # Cria o novo cadastro do cliente com saldo zero
    with open('cashback.csv', 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([cpf, nome, cidade, 0])

    print("Cliente cadastrado com sucesso!")


def consultar_saldo():
    cpf = input("Digite o CPF do cliente: ")

    # Busca o saldo do cliente
    with open('cashback.csv', 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            if cpf == row[0]:
                print("Saldo do cliente:", row[3])
                return

    print("Cliente não encontrado.")


def adicionar_compra():
    cpf = input("Digite o CPF do cliente: ")
    valor_compra = float(input("Digite o valor da compra: "))

    # Atualiza o cashback do cliente
    rows = []
    with open('cashback.csv', 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            if cpf == row[0]:
                row[3] = str(float(row[3]) + (valor_compra * 0.02))
            rows.append(row)

    with open('cashback.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(rows)

    print("Compra adicionada com sucesso.")


def utilizar_saldo():
    cpf = input("Digite o CPF do cliente: ")
    valor_utilizado = float(input("Digite o valor a ser utilizado do saldo: "))

    # Atualiza o cashback do cliente
    rows = []
    with open('cashback.csv', 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            if cpf == row[0]:
                if valor_utilizado <= float(row[3]):
                    row[3] = str(float(row[3]) - valor_utilizado)
                else:
                    print("Saldo insuficiente.")
                    return
            rows.append(row)

    with open('cashback.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(rows)

    print("Saldo utilizado com sucesso.")

# Função principal do programa


def main():
    while True:
        print("\nMenu:")
        print("1 - Cadastrar cliente")
        print("2 - Consultar saldo")
        print("3 - Adicionar compra")
        print("4 - Utilizar saldo")
        print("0 - Sair")

        opcao = input("Digite a opção desejada: ")

        if opcao == '1':
            cadastrar_cliente()
        elif opcao == '2':
            consultar_saldo()
        elif opcao == '3':
            adicionar_compra()
        elif opcao == '4':
            utilizar_saldo()
        elif opcao == '0':
            break
        else:
            print("Opção inválida. Por favor, tente novamente.")

        voltar_menu = input("Deseja voltar ao menu principal? (s/n): ")
        if voltar_menu.lower() != 's':
            break


if __name__ == '__main__':
    main()
