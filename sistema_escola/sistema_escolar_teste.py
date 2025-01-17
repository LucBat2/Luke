import tkinter as tk
from tkinter import ttk, messagebox
from ttkthemes import ThemedTk
from tkinterweb import HtmlFrame  # Para exibir páginas HTML
import pandas as pd
import os
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import time
import requests
from PIL import Image, ImageTk

# Configurações iniciais e banco de dados
DATABASE_FILE = "alunos.xlsx"
def verificar_banco():
    if not os.path.exists(DATABASE_FILE):
        df = pd.DataFrame(columns=["Matricula", "Nome", "Presenças", "Faltas", "Observações", "Atividades"])
        df.to_excel(DATABASE_FILE, index=False)

verificar_banco()

def carregar_alunos():
    return pd.read_excel(DATABASE_FILE)

def salvar_alunos(df):
    df.to_excel(DATABASE_FILE, index=False)

# Funções principais
def registrar_presenca(matricula, presente=True):
    df = carregar_alunos()
    if matricula in df["Matricula"].values:
        if presente:
            df.loc[df["Matricula"] == matricula, "Presenças"] += 1
        else:
            df.loc[df["Matricula"] == matricula, "Faltas"] += 1
        salvar_alunos(df)
        messagebox.showinfo("Sucesso", "Presença/Falta registrada com sucesso!")
    else:
        messagebox.showerror("Erro", "Matrícula não encontrada.")

def adicionar_observacao(matricula, observacao):
    df = carregar_alunos()
    if matricula in df["Matricula"].values:
        df.loc[df["Matricula"] == matricula, "Observações"] = observacao
        salvar_alunos(df)
        messagebox.showinfo("Sucesso", "Observação adicionada com sucesso!")
    else:
        messagebox.showerror("Erro", "Matrícula não encontrada.")

def registrar_atividade(matricula, atividade):
    df = carregar_alunos()
    if matricula in df["Matricula"].values:
        df.loc[df["Matricula"] == matricula, "Atividades"] = atividade
        salvar_alunos(df)
        messagebox.showinfo("Sucesso", "Atividade registrada com sucesso!")
    else:
        messagebox.showerror("Erro", "Matrícula não encontrada.")

def emitir_relatorio():
    df = carregar_alunos()
    figure = Figure(figsize=(6, 4), dpi=100)
    ax = figure.add_subplot(111)
    df["Presenças"].plot(kind="bar", ax=ax, label="Presenças", color="green")
    df["Faltas"].plot(kind="bar", ax=ax, label="Faltas", color="red")
    ax.set_title("Relatório de Presenças e Faltas")
    ax.set_xlabel("Alunos")
    ax.set_ylabel("Total")
    ax.legend()

    return figure

# Tela de Login com WebView
def tela_login(root, on_login_success):
    def autenticar():
        usuario = entry_usuario.get()
        senha = entry_senha.get()
        if usuario == "admin" and senha == "123":
            animacao_transicao()
            on_login_success()
        else:
            messagebox.showerror("Erro", "Usuário ou senha incorretos.")

    def animacao_transicao():
        for i in range(800):
            frame_login.place(x=-i, y=0)
            frame_login.update()
            time.sleep(0.001)

    frame_login = ttk.Frame(root, padding=20)
    frame_login.place(x=800, y=0, width=400, height=600)

    background_img = Image.open("backgroud.jpg").resize((1024, 768))
    background_photo = ImageTk.PhotoImage(background_img)
    bg_label = tk.Label(root, image=background_photo)
    bg_label.image = background_photo
    bg_label.place(x=0, y=0, relwidth=1, relheight=1)

    ttk.Label(frame_login, text="Login", font=("Segoe UI", 20, "bold"), foreground="blue").pack(pady=20)

    ttk.Label(frame_login, text="Usuário:", foreground="red").pack(pady=5)
    entry_usuario = ttk.Entry(frame_login)
    entry_usuario.pack(pady=5)

    ttk.Label(frame_login, text="Senha:", foreground="red").pack(pady=5)
    entry_senha = ttk.Entry(frame_login, show="*")
    entry_senha.pack(pady=5)

    ttk.Button(frame_login, text="Entrar", command=autenticar).pack(pady=20)

# Interface gráfica
class SistemaEscola:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema Escolar - HUD Estilo Windows 11")
        self.root.geometry("1024x768")

        style = ttk.Style()
        style.theme_use('clam')
        style.configure('TButton', font=('Segoe UI', 10), padding=10)

        tela_login(self.root, self.iniciar_sistema)

    def iniciar_sistema(self):
        self.frame_menu = ttk.Frame(self.root, padding=10)
        self.frame_menu.pack(side="left", fill="y")

        ttk.Label(self.frame_menu, text="Menu", font=("Segoe UI", 14, "bold"), foreground="blue").pack(pady=10)

        self.btn_presenca = ttk.Button(self.frame_menu, text="Presença", command=self.tela_presenca)
        self.btn_presenca.pack(pady=5, fill="x")

        self.btn_observacao = ttk.Button(self.frame_menu, text="Observação", command=self.tela_observacao)
        self.btn_observacao.pack(pady=5, fill="x")

        self.btn_atividade = ttk.Button(self.frame_menu, text="Atividade", command=self.tela_atividade)
        self.btn_atividade.pack(pady=5, fill="x")

        self.btn_relatorio = ttk.Button(self.frame_menu, text="Relatório", command=self.tela_relatorio)
        self.btn_relatorio.pack(pady=5, fill="x")

        self.frame_conteudo = ttk.Frame(self.root, padding=10)
        self.frame_conteudo.pack(side="right", expand=True, fill="both")

        self.bind_teclas_atalho()

    def bind_teclas_atalho(self):
        self.root.bind("<F1>", lambda e: self.tela_presenca())
        self.root.bind("<F2>", lambda e: self.tela_observacao())
        self.root.bind("<F3>", lambda e: self.tela_atividade())
        self.root.bind("<F4>", lambda e: self.tela_relatorio())

    def limpar_conteudo(self):
        for widget in self.frame_conteudo.winfo_children():
            widget.destroy()

    def tela_presenca(self):
        self.limpar_conteudo()
        ttk.Label(self.frame_conteudo, text="Registrar Presença/Falta", font=("Segoe UI", 14, "bold"), foreground="blue").pack(pady=10)

        frame_form = ttk.Frame(self.frame_conteudo)
        frame_form.pack(pady=20)

        ttk.Label(frame_form, text="Matrícula:", foreground="red").grid(row=0, column=0, padx=5, pady=5)
        matricula_entry = ttk.Entry(frame_form)
        matricula_entry.grid(row=0, column=1, padx=5, pady=5)

        ttk.Button(frame_form, text="Presente", command=lambda: registrar_presenca(matricula_entry.get(), True)).grid(row=1, column=0, pady=10)
        ttk.Button(frame_form, text="Falta", command=lambda: registrar_presenca(matricula_entry.get(), False)).grid(row=1, column=1, pady=10)

    def tela_observacao(self):
        self.limpar_conteudo()
        ttk.Label(self.frame_conteudo, text="Adicionar Observação", font=("Segoe UI", 14, "bold"), foreground="blue").pack(pady=10)

        frame_form = ttk.Frame(self.frame_conteudo)
        frame_form.pack(pady=20)

        ttk.Label(frame_form, text="Matrícula:", foreground="red").grid(row=0, column=0, padx=5, pady=5)
        matricula_entry = ttk.Entry(frame_form)
        matricula_entry.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(frame_form, text="Observação:", foreground="red").grid(row=1, column=0, padx=5, pady=5)
        observacao_entry = ttk.Entry(frame_form)
        observacao_entry.grid(row=1, column=1, padx=5, pady=5)

        ttk.Button(frame_form, text="Salvar", command=lambda: adicionar_observacao(matricula_entry.get(), observacao_entry.get())).grid(row=2, columnspan=2, pady=10)

    def tela_atividade(self):
        self.limpar_conteudo()
        ttk.Label(self.frame_conteudo, text="Registrar Atividade", font=("Segoe UI", 14, "bold"), foreground="blue").pack(pady=10)

        frame_form = ttk.Frame(self.frame_conteudo)
        frame_form.pack(pady=20)

        ttk.Label(frame_form, text="Matrícula:", foreground="red").grid(row=0, column=0, padx=5, pady=5)
        matricula_entry = ttk.Entry(frame_form)
        matricula_entry.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(frame_form, text="Atividade:", foreground="red").grid(row=1, column=0, padx=5, pady=5)
        atividade_entry = ttk.Entry(frame_form)
        atividade_entry.grid(row=1, column=1, padx=5, pady=5)

        ttk.Button(frame_form, text="Salvar", command=lambda: registrar_atividade(matricula_entry.get(), atividade_entry.get())).grid(row=2, columnspan=2, pady=10)

    def tela_relatorio(self):
        self.limpar_conteudo()
        ttk.Label(self.frame_conteudo, text="Relatório de Presenças e Faltas", font=("Segoe UI", 14, "bold"), foreground="blue").pack(pady=10)

        figure = emitir_relatorio()
        canvas = FigureCanvasTkAgg(figure, master=self.frame_conteudo)
        canvas.draw()
        canvas.get_tk_widget().pack()

if __name__ == "__main__":
    root = ThemedTk(theme="arc")
    app = SistemaEscola(root)
