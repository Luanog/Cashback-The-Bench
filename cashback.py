import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import gspread
from google.oauth2.service_account import Credentials
from PIL import ImageTk, Image
from ttkthemes import ThemedStyle

scope = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']
credentials = Credentials.from_service_account_file(
    'C:\\Users\\admin\\Desktop\\Projetos Luan\\Projetos Python\\Cashback\\cashback-the-bench-401520-171538fa2e32.json', scopes=scope)
client = gspread.authorize(credentials)
SAMPLE_SPREADSHEET_ID = '1FzBe8Us-Z9Nh4bh2wHEI8OJ7CMZpaGd-4w7ncnEaCzo'
SAMPLE_RANGE_NAME = 'Página1!A1:E'


class App:
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
        header_frame = tk.Frame(self.janela, bg="black")
        header_frame.pack(fill="x")
        header_label = ttk.Label(header_frame, text="CASHBACK", font=(
            "Arial", 36, "bold"), background="black", foreground="white")
        header_label.pack(pady=10)
        menu_frame = tk.Frame(self.janela, bg="white")
        menu_frame.pack(fill="both", padx=10, pady=10)
        self.botao_cadastrar = ttk.Button(
            menu_frame, text="Cadastrar Cliente", command=self.abrir_janela_cadastrar)
        self.botao_cadastrar.image = ImageTk.PhotoImage(
            Image.open("adicionar cadastro icone.png").resize((24, 24)))
        self.botao_cadastrar.config(
            image=self.botao_cadastrar.image, compound="left")
        self.botao_cadastrar.pack(pady=10, side="top")
        self.botao_consultar = ttk.Button(
            menu_frame, text="Consultar Saldo", command=self.abrir_janela_consultar)
        self.botao_consultar.image = ImageTk.PhotoImage(
            Image.open("Consultar icone.png").resize((24, 24)))
        self.botao_consultar.config(
            image=self.botao_consultar.image, compound="left")
        self.botao_consultar.pack(pady=10, side="top")
        self.botao_adicionar = ttk.Button(
            menu_frame, text="Adicionar Compra", command=self.abrir_janela_adicionar)
        self.botao_adicionar.image = ImageTk.PhotoImage(
            Image.open("adicionar compra icone.png").resize((24, 24)))
        self.botao_adicionar.config(
            image=self.botao_adicionar.image, compound="left")
        self.botao_adicionar.pack(pady=10, side="top")
        self.botao_utilizar = ttk.Button(
            menu_frame, text="Utilizar Saldo", command=self.abrir_janela_utilizar)
        self.botao_utilizar.image = ImageTk.PhotoImage(
            Image.open("utilizar saldo icone.png").resize((24, 24)))
        self.botao_utilizar.config(
            image=self.botao_utilizar.image, compound="left")
        self.botao_utilizar.pack(pady=10, side="top")
        logo_image = Image.open("Logotipo  The Bench horizontal.png")
        logo_image = logo_image.resize((250, 40))
        logo_photo = ImageTk.PhotoImage(logo_image)
        logo_label = ttk.Label(menu_frame, image=logo_photo)
        logo_label.pack(pady=10)
        self.janela.mainloop()

    def abrir_janela_cadastrar(self):
        janela_cadastrar = tk.Toplevel(self.janela)
        janela_cadastrar.title("Cadastrar Cliente")
        janela_cadastrar.geometry("500x400")
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
        botao_confirmar = ttk.Button(janela_cadastrar, text="Confirmar", command=lambda: self.cadastrar_cliente(
            entry_cpf.get(), entry_nome.get(), entry_cidade.get()), style="TButton")
        botao_confirmar.pack(pady=10)

    def cadastrar_cliente(self, cpf, nome, cidade):
        messagebox.showinfo("Sucesso", "Cliente cadastrado com sucesso!")

    def abrir_janela_consultar(self):
        janela_consultar = tk.Toplevel(self.janela)
        janela_consultar.title("Consultar Saldo")
        janela_consultar.geometry("400x300")
        janela_consultar.configure(bg="white")
        label_cpf = ttk.Label(janela_consultar, text="CPF:",
                              background="white", foreground="black", font=("Arial", 16))
        label_cpf.pack(pady=10)
        entry_cpf = ttk.Entry(janela_consultar, width=30, font=("Arial", 16))
        entry_cpf.pack(pady=10)
        botao_confirmar = ttk.Button(janela_consultar, text="Confirmar",
                                     command=lambda: self.consultar_saldo(entry_cpf.get()), style="TButton")
        botao_confirmar.pack(pady=10)

    def consultar_saldo(self, cpf):
        if cpf in self.cpf_list:
            row_index = self.cpf_list.index(cpf) + 1
            saldo = float(self.sheet.cell(row_index, 4).value)
            messagebox.showinfo("Saldo", f"Saldo do cliente {
                                self.sheet.cell(row_index, 2).value}: R${saldo:.2f}")
        else:
            messagebox.showerror("Erro", "Cliente não encontrado.")

    def abrir_janela_adicionar(self):
        janela_adicionar = tk.Toplevel(self.janela)
        janela_adicionar.title("Adicionar Compra")
        janela_adicionar.geometry("400x300")
        janela_adicionar.configure(bg="white")
        label_cpf = ttk.Label(janela_adicionar, text="CPF:",
                              background="white", foreground="black", font=("Arial", 16))
        label_cpf.pack(pady=10)
        entry_cpf = ttk.Entry(janela_adicionar, width=30, font=("Arial", 16))
        entry_cpf.pack(pady=10)
        label_valor = ttk.Label(janela_adicionar, text="Valor:",
                                background="white", foreground="black", font=("Arial", 16))
        label_valor.pack(pady=10)
        entry_valor = ttk.Entry(janela_adicionar, width=30, font=("Arial", 16))
        entry_valor.pack(pady=10)
        botao_confirmar = ttk.Button(janela_adicionar, text="Confirmar", command=lambda: self.adicionar_compra(
            entry_cpf.get(), float(entry_valor.get())), style="TButton")
        botao_confirmar.pack(pady=10)

    def adicionar_compra(self, cpf, valor_compra):
        if cpf in self.cpf_list:
            row_index = self.cpf_list.index(cpf) + 1
            saldo = float(self.sheet.cell(row_index, 4).value)
            self.sheet.update_cell(row_index, 4, str(
                saldo + (valor_compra * 0.02)))
            nome_cliente = self.sheet.cell(row_index, 2).value
            novo_saldo = self.sheet.cell(row_index, 4).value
            messagebox.showinfo("Sucesso", f"Compra adicionada com sucesso para {
                                nome_cliente}.\nNovo saldo: R${novo_saldo}")
        else:
            messagebox.showerror("Erro", "Cliente não encontrado.")

    def abrir_janela_utilizar(self):
        janela_utilizar = tk.Toplevel(self.janela)
        janela_utilizar.title("Utilizar Saldo")
        janela_utilizar.geometry("400x300")
        janela_utilizar.configure(bg="white")
        label_cpf = ttk.Label(janela_utilizar, text="CPF:",
                              background="white", foreground="black", font=("Arial", 16))
        label_cpf.pack(pady=10)
        entry_cpf = ttk.Entry(janela_utilizar, width=30, font=("Arial", 16))
        entry_cpf.pack(pady=10)
        label_valor = ttk.Label(janela_utilizar, text="Valor:",
                                background="white", foreground="black", font=("Arial", 16))
        label_valor.pack(pady=10)
        entry_valor = ttk.Entry(janela_utilizar, width=30, font=("Arial", 16))
        entry_valor.pack(pady=10)
        botao_confirmar = ttk.Button(janela_utilizar, text="Confirmar", command=lambda: self.utilizar_saldo(
            entry_cpf.get(), float(entry_valor.get())), style="TButton")
        botao_confirmar.pack(pady=10)

    def utilizar_saldo(self, cpf, valor_utilizado):
        if cpf in self.cpf_list:
            row_index = self.cpf_list.index(cpf) + 1
            saldo = float(self.sheet.cell(row_index, 4).value)
            self.sheet.update_cell(row_index, 4, str(saldo - valor_utilizado))
            if valor_utilizado <= saldo:
                nome_cliente = self.sheet.cell(row_index, 2).value
                novo_saldo = self.sheet.cell(row_index, 4).value
                messagebox.showinfo("Sucesso", f"Saldo utilizado com sucesso para {
                                    nome_cliente}.\nNovo saldo: R${novo_saldo}")
            else:
                messagebox.showerror("Erro", "Saldo insuficiente.")
        else:
            messagebox.showerror("Erro", "Cliente não encontrado.")


App()
