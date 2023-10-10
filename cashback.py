import gspread
from google.oauth2.service_account import Credentials

scope = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']
credentials = Credentials.from_service_account_file(
    'C:\\Users\\admin\\Desktop\\Projetos Luan\\Projetos Python\\Cashback\\cashback-the-bench-json-1ff0645ee92a.json', scopes=scope)
client = gspread.authorize(credentials)

SAMPLE_SPREADSHEET_ID = '1FzBe8Us-Z9Nh4bh2wHEI8OJ7CMZpaGd-4w7ncnEaCzo'
SAMPLE_RANGE_NAME = 'Página1!A1:E'


def cadastrar_cliente():
    planilha = client.open_by_key(SAMPLE_SPREADSHEET_ID)
    sheet = planilha.get_worksheet(0)
    cpf = input("Digite o CPF do cliente: ")
    nome = input("Digite o nome do cliente: ")
    cidade = input("Digite a cidade do cliente: ")

    cpf_list = sheet.col_values(1)
    if cpf in cpf_list:
        print("CPF já cadastrado. Por favor, tente novamente.")
        return

    sheet.append_row([cpf, nome, cidade, 0])
    print("Cliente cadastrado com sucesso!")


def consultar_saldo():
    planilha = client.open_by_key(SAMPLE_SPREADSHEET_ID)
    sheet = planilha.get_worksheet(0)
    cpf = input("Digite o CPF do cliente: ")

    cpf_list = sheet.col_values(1)
    if cpf in cpf_list:
        row_index = cpf_list.index(cpf) + 1
        saldo = float(sheet.cell(row_index, 4).value)
        print(f"Saldo do cliente {sheet.cell(
            row_index, 2).value}: R${saldo:.2f}")
    else:
        print("Cliente não encontrado.")


def adicionar_compra():
    planilha = client.open_by_key(SAMPLE_SPREADSHEET_ID)
    sheet = planilha.get_worksheet(0)
    cpf = input("Digite o CPF do cliente: ")
    valor_compra = float(input("Digite o valor da compra: "))

    cpf_list = sheet.col_values(1)
    if cpf in cpf_list:
        row_index = cpf_list.index(cpf) + 1
        saldo = float(sheet.cell(row_index, 4).value)
        sheet.update_cell(row_index, 4, str(saldo + (valor_compra * 0.02)))
        print("Compra adicionada com sucesso.")
    else:
        print("Cliente não encontrado.")


def utilizar_saldo():
    planilha = client.open_by_key(SAMPLE_SPREADSHEET_ID)
    sheet = planilha.get_worksheet(0)
    cpf = input("Digite o CPF do cliente: ")
    valor_utilizado = float(input("Digite o valor a ser utilizado do saldo: "))

    cpf_list = sheet.col_values(1)
    if cpf in cpf_list:
        row_index = cpf_list.index(cpf) + 1
        saldo = float(sheet.cell(row_index, 4).value)
        if valor_utilizado <= saldo:
            sheet.update_cell(row_index, 4, str(saldo - valor_utilizado))
            print("Saldo utilizado com sucesso.")
        else:
            print("Saldo insuficiente.")
    else:
        print("Cliente não encontrado.")


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
