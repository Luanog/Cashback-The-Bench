import tkinter as tk
import datetime
from tkinter import messagebox, ttk
from gspread import authorize
from google.oauth2.service_account import Credentials
from PIL import ImageTk, Image
from ttkthemes import ThemedStyle

# Define o escopo e as credenciais para a API do Google Sheets
scope = [
    'https://spreadsheets.google.com/feeds',
    'https://www.googleapis.com/auth/drive'
]

credentials = Credentials.from_service_account_file(
    'C:\\Users\\admin\\Desktop\\Projetos Luan\\Projetos Python\\Cashback\\cashback-the-bench-401520-171538fa2e32.json',
    scopes=scope
)

# Autoriza o cliente
client = authorize(credentials)

# Define o ID da planilha e a faixa
SAMPLE_SPREADSHEET_ID = '1FzBe8Us-Z9Nh4bh2wHEI8OJ7CMZpaGd-4w7ncnEaCzo'
SAMPLE_RANGE_NAME = 'Página1!A1:E'


class App:
    """
    Classe principal da aplicação.
    """

    def __init__(self):
        self.janela = tk.Tk()
        self.janela.title("Cashback The Bench")
        self.janela.configure(bg="white")
        self.janela.geometry("854x480")
        self.style = ThemedStyle(self.janela)
        self.style.set_theme("black")
        self.style.configure("TLabel", font=("Arial", 24),
                             background="white", foreground="black")
        self.style.configure("TEntry", font=("Arial", 24),
                             background="white", foreground="black")
        self.style.configure("TButton", font=("Arial", 24), background="white", foreground="black",
                             relief="sunken", width=20, borderwidth=5, bordercolor="black", anchor="center")
        self.planilha = client.open_by_key(SAMPLE_SPREADSHEET_ID)
        self.sheet = self.planilha.get_worksheet(0)
        self.cpf_list = self.sheet.col_values(1)

        # Crie o frame do cabeçalho e o rótulo
        header_frame = tk.Frame(self.janela, bg="black")
        header_frame.pack(fill="x")
        header_label = ttk.Label(header_frame, text="CASHBACK", font=("Arial", 36, "bold"), background="black",
                                 foreground="white")
        header_label.pack(pady=10)

        # Crie o frame do menu
        menu_frame = tk.Frame(self.janela, bg="white")
        menu_frame.pack(fill="both", padx=10, pady=10)

        # Crie botões para diferentes ações
        self.botao_cadastrar = ttk.Button(
            menu_frame, text="Cadastrar Cliente", command=self.abrir_janela_cadastrar)
        self.botao_cadastrar.image = ImageTk.PhotoImage(
            Image.open("C:/Users/admin/Desktop/Projetos Luan/Projetos Python/Cashback/adicionar cadastro icone.png").resize((24, 24)))
        self.botao_cadastrar.config(
            image=self.botao_cadastrar.image, compound="left")
        self.botao_cadastrar.pack(pady=10, side="top")

        self.botao_consultar = ttk.Button(
            menu_frame, text="Consultar Saldo", command=self.abrir_janela_consultar)
        self.botao_consultar.image = ImageTk.PhotoImage(
            Image.open("C:/Users/admin/Desktop/Projetos Luan/Projetos Python/Cashback/Consultar icone.png").resize((24, 24)))
        self.botao_consultar.config(
            image=self.botao_consultar.image, compound="left")
        self.botao_consultar.pack(pady=10, side="top")

        self.botao_adicionar = ttk.Button(
            menu_frame, text="Adicionar Compra", command=self.abrir_janela_adicionar)
        self.botao_adicionar.image = ImageTk.PhotoImage(
            Image.open("C:/Users/admin/Desktop/Projetos Luan/Projetos Python/Cashback/adicionar compra icone.png").resize((24, 24)))
        self.botao_adicionar.config(
            image=self.botao_adicionar.image, compound="left")
        self.botao_adicionar.pack(pady=10, side="top")

        self.botao_utilizar = ttk.Button(
            menu_frame, text="Utilizar Saldo", command=self.abrir_janela_utilizar)
        self.botao_utilizar.image = ImageTk.PhotoImage(
            Image.open("C:/Users/admin/Desktop/Projetos Luan/Projetos Python/Cashback/utilizar saldo icone.png").resize((24, 24)))
        self.botao_utilizar.config(
            image=self.botao_utilizar.image, compound="left")
        self.botao_utilizar.pack(pady=10, side="top")

        # Crie o rótulo do logo
        logo_image = Image.open(
            "C://Users//admin//Desktop//Projetos Luan//Projetos Python//Cashback//Logotipo  The Bench horizontal.png")
        logo_image = logo_image.resize((250, 40))
        logo_photo = ImageTk.PhotoImage(logo_image)
        logo_label = ttk.Label(menu_frame, image=logo_photo)
        logo_label.pack(pady=10)

        self.janela.mainloop()

    def abrir_janela_cadastrar(self):
        """
        Abre uma janela para cadastrar um cliente.
        """
        janela_cadastrar = tk.Toplevel(self.janela)
        janela_cadastrar.title("Cadastrar Cliente")
        janela_cadastrar.geometry("500x500")

        label_cpf = ttk.Label(
            janela_cadastrar, text="CPF:", font=("Arial", 16))
        label_cpf.pack(pady=10)

        entry_cpf = ttk.Entry(janela_cadastrar, width=30, font=("Arial", 16))
        entry_cpf.pack(pady=10)

        label_nome = ttk.Label(
            janela_cadastrar, text="Nome:", font=("Arial", 16))
        label_nome.pack(pady=10)

        entry_nome = ttk.Entry(janela_cadastrar, width=30, font=("Arial", 16))
        entry_nome.pack(pady=10)

        label_cidade = ttk.Label(
            janela_cadastrar, text="Cidade:", font=("Arial", 16))
        label_cidade.pack(pady=10)

        entry_cidade = ttk.Entry(
            janela_cadastrar, width=30, font=("Arial", 16))
        entry_cidade.pack(pady=10)

        label_telefone = ttk.Label(
            janela_cadastrar, text="Telefone:", font=("Arial", 16))
        label_telefone.pack(pady=10)

        entry_telefone = ttk.Entry(
            janela_cadastrar, width=30, font=("Arial", 16))
        entry_telefone.pack(pady=10)

        botao_confirmar = ttk.Button(janela_cadastrar, text="Confirmar",
                                     command=lambda: self.cadastrar_cliente(entry_cpf.get(), entry_nome.get(), entry_cidade.get(), entry_telefone.get(), janela_cadastrar), style="TButton")
        botao_confirmar.pack(pady=10)

    def cadastrar_cliente(self, cpf, nome, cidade, telefone, janela_cadastrar):
        """
        Cadastra um cliente com CPF, nome, cidade e telefone fornecidos.
        """
        if cpf in self.cpf_list:
            messagebox.showerror("Erro", "Cliente já cadastrado.")
        else:
            next_row = len(self.sheet.get_all_values()) + 1
            self.sheet.update(f'A{next_row}', cpf)
            self.sheet.update(f'B{next_row}', nome)
            self.sheet.update(f'C{next_row}', cidade)
            self.sheet.update(f'D{next_row}', telefone)
            self.sheet.update(f'E{next_row}', '0.00')
            messagebox.showinfo("Sucesso", "Cliente cadastrado com sucesso!")
        janela_cadastrar.destroy()  # Adiciona essa linha para fechar a janela

    def abrir_janela_consultar(self):
        """
        Abre uma janela para consultar o saldo de um cliente.
        """
        self.janela_consultar = tk.Toplevel(self.janela)
        self.janela_consultar.title("Consultar Saldo")
        self.janela_consultar.geometry("400x300")
        self.janela_consultar.configure(bg="white")
        label_cpf = ttk.Label(self.janela_consultar, text="CPF:", background="white", foreground="black",
                              font=("Arial", 16))
        label_cpf.pack(pady=10)
        entry_cpf = ttk.Entry(self.janela_consultar,
                              width=30, font=("Arial", 16))
        entry_cpf.pack(pady=10)
        botao_confirmar = ttk.Button(self.janela_consultar, text="Confirmar",
                                     command=lambda: self.consultar_saldo(entry_cpf.get(), self.janela_consultar), style="TButton")
        botao_confirmar.pack(pady=10)

    def consultar_saldo(self, cpf, janela_consultar):
        """
        Consulta o saldo de um cliente com o CPF fornecido.
        """
        if cpf in self.cpf_list:
            row_index = self.cpf_list.index(cpf) + 1
            saldo = float(self.sheet.cell(row_index, 5).value)
            messagebox.showinfo("Saldo", f"Saldo do cliente {
                                self.sheet.cell(row_index, 2).value}: R${saldo:.2f}")
            janela_consultar.destroy()  # Adiciona essa linha para fechar a janela
        else:
            messagebox.showerror("Erro", "Cliente não encontrado.")

    def abrir_janela_adicionar(self):
        """
        Abre uma janela para adicionar uma compra para um cliente.
        """
        janela_adicionar = tk.Toplevel(self.janela)
        janela_adicionar.title("Adicionar Compra")
        janela_adicionar.geometry("400x300")
        label_cpf = ttk.Label(janela_adicionar, text="CPF:", background="white", foreground="black",
                              font=("Arial", 16))
        label_cpf.pack(pady=10)
        entry_cpf = ttk.Entry(janela_adicionar, width=30, font=("Arial", 16))
        entry_cpf.pack(pady=10)
        label_valor = ttk.Label(janela_adicionar, text="Valor:", background="white", foreground="black",
                                font=("Arial", 16))
        label_valor.pack(pady=10)
        entry_valor = ttk.Entry(janela_adicionar, width=30, font=("Arial", 16))
        entry_valor.pack(pady=10)
        botao_confirmar = ttk.Button(janela_adicionar, text="Confirmar",
                                     command=lambda: self.adicionar_compra(entry_cpf.get(), float(entry_valor.get()), janela_adicionar), style="TButton")
        botao_confirmar.pack(pady=10)

    def adicionar_compra(self, cpf, valor_compra, janela_adicionar):
        if cpf in self.cpf_list:
            row_index = self.cpf_list.index(cpf) + 1
            cashback_celula = self.sheet.cell(row_index, 5).value
            if cashback_celula is None or cashback_celula == '':
                cashback = 0.0
            else:
                cashback = float(cashback_celula)
            cashback += valor_compra * 0.02  # Calcula o valor de cashback atualizado

            # Atualiza a coluna "cashback" com o novo valor
            self.sheet.update(f'E{row_index}', f'{cashback:.2f}')

            entradas_celula = self.sheet.cell(row_index, 6).value
            if entradas_celula is None or entradas_celula == '':
                entradas = ''
            else:
                entradas = entradas_celula

            if entradas != '':
                entradas += ' | '  # Adiciona um caractere separador se já existir valor na coluna "entradas"

            data_hora_atual = datetime.datetime.now().strftime("%d/%m/%Y %H:%M")
            # Adiciona a data, hora e valor da compra à coluna "entradas"
            entradas += f'{data_hora_atual} - R${valor_compra * 0.02:.2f}'

            # Atualiza a coluna "entradas" com o novo valor
            self.sheet.update(f'F{row_index}', entradas)

            nome_cliente = self.sheet.cell(row_index, 2).value
            messagebox.showinfo('Sucesso', f'Compra adicionada com sucesso para {
                                nome_cliente}.\nNovo cashback: R${cashback:.2f}')
        else:
            messagebox.showerror('Erro', 'Cliente não encontrado.')

        janela_adicionar.destroy()  # Fecha a janela

    def abrir_janela_utilizar(self):
        """
        Abre uma janela para utilizar o saldo de um cliente.
        """
        janela_utilizar = tk.Toplevel(self.janela)
        janela_utilizar.title("Utilizar Saldo")
        janela_utilizar.geometry("400x300")
        label_cpf = ttk.Label(janela_utilizar, text="CPF:", background="white", foreground="black",
                              font=("Arial", 16))
        label_cpf.pack(pady=10)
        entry_cpf = ttk.Entry(janela_utilizar, width=30, font=("Arial", 16))
        entry_cpf.pack(pady=10)
        label_valor = ttk.Label(janela_utilizar, text="Valor:", background="white", foreground="black",
                                font=("Arial", 16))
        label_valor.pack(pady=10)
        entry_valor = ttk.Entry(janela_utilizar, width=30, font=("Arial", 16))
        entry_valor.pack(pady=10)
        botao_confirmar = ttk.Button(janela_utilizar, text="Confirmar",
                                     command=lambda: self.utilizar_saldo(entry_cpf.get(), float(entry_valor.get()), janela_utilizar), style="TButton")
        botao_confirmar.pack(pady=10)

    def utilizar_saldo(self, cpf, valor_utilizado, janela_utilizar):
        if cpf in self.cpf_list:
            row_index = self.cpf_list.index(cpf) + 1
            saldo = float(self.sheet.cell(row_index, 5).value)
            if valor_utilizado <= saldo:
                self.sheet.update_cell(
                    row_index, 5, str(saldo - valor_utilizado))
                data_hora_atual = datetime.datetime.now().strftime("%d/%m/%Y %H:%M")
                movimentacao = f"{data_hora_atual} - R${valor_utilizado:.2f}"
                saidas_celula = self.sheet.cell(row_index, 7).value
                if saidas_celula is None or saidas_celula == '':
                    saidas = ""
                else:
                    saidas = saidas_celula
                if saidas != "":
                    saidas += " | "
                saidas += movimentacao
                self.sheet.update(f"G{row_index}", saidas)
                nome_cliente = self.sheet.cell(row_index, 2).value
                novo_saldo = self.sheet.cell(row_index, 5).value
                messagebox.showinfo("Sucesso", f"Saldo utilizado com sucesso para {
                                    nome_cliente}.\nNovo saldo: R${novo_saldo}")
                janela_utilizar.destroy()  # Fechar a janela 'janela_utilizar'
            else:
                messagebox.showerror("Erro", "Saldo insuficiente.")
        else:
            messagebox.showerror("Erro", "Cliente não encontrado.")


# Create an instance of the App class
app = App()
