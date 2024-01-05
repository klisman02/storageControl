from controleDeEstoque import Gestao

import tkinter as tk
from tkinter import messagebox
import sqlite3

class Gestao:
    def __init__(self, banco):
        self.conn = sqlite3.connect(banco)
        self.criar_tabela_estoque()

    def criar_tabela_estoque(self):
        cursor = self.conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS estoque (
                id INTEGER PRIMARY KEY,
                produto TEXT,
                quantidade INTEGER
            )
        ''')
        self.conn.commit()

    def adicionar_produto(self, produto, quantidade):
        cursor = self.conn.cursor()
        cursor.execute(
            "INSERT INTO estoque (produto, quantidade) VALUES (?, ?)", (produto, quantidade)
        )
        self.conn.commit()

    def remover_produto(self, produto, quantidade):
        cursor = self.conn.cursor()
        cursor.execute(
            "SELECT quantidade FROM estoque WHERE produto=?", (produto,))
        resultado = cursor.fetchone()
        if resultado:
            estoque_atual = resultado[0]
            if estoque_atual >= quantidade:
                cursor.execute("UPDATE estoque SET quantidade=? WHERE produto=?", 
                            (estoque_atual - quantidade, produto))
                self.conn.commit()
            else:
                print(f"Quantidade insuficiente de {produto} em estoque.")
        else:
            print(f"{produto} não encontrado em estoque.")

    def consultar_estoque(self, produto):
        cursor = self.conn.cursor()
        cursor.execute(
            "SELECT quantidade FROM estoque WHERE produto=?", (produto,))
        resultado = cursor.fetchone()
        if resultado:
            return resultado[0]
        else:
            return 0

    def listar_produtos(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT produto FROM estoque")
        produtos = cursor.fetchall()
        return [produto[0] for produto in produtos]

class InterfaceGestao(tk.Tk):
    def __init__(self, sistema):
        super().__init__()
        self.sistema = sistema
        self.title("Gestão de Estoque")

        # Componentes da interface
        self.label_produto = tk.Label(self, text="Produto:")
        self.entry_produto = tk.Entry(self)
        self.label_quantidade = tk.Label(self, text="Quantidade:")
        self.entry_quantidade = tk.Entry(self)
        self.button_adicionar = tk.Button(self, text="Adicionar Produto", command=self.adicionar_produto)
        self.button_listar = tk.Button(self, text="Listar Produtos", command=self.listar_produtos)

        self.label_produto.grid(row=0, column=0, padx=10, pady=5, sticky=tk.W)
        self.entry_produto.grid(row=0, column=1, padx=10, pady=5)
        self.label_quantidade.grid(row=1, column=0, padx=10, pady=5, sticky=tk.W)
        self.entry_quantidade.grid(row=1, column=1, padx=10, pady=5)
        self.button_adicionar.grid(row=2, column=0, columnspan=2, pady=10)
        self.button_listar.grid(row=3, column=0, columnspan=2, pady=10)

    def adicionar_produto(self):
        produto = self.entry_produto.get()
        quantidade = int(self.entry_quantidade.get())

        self.sistema.adicionar_produto(produto, quantidade)

        messagebox.showinfo("Sucesso", f"Produto {produto} adicionado com sucesso!")

    def listar_produtos(self):
        produtos = self.sistema.listar_produtos()
        mensagem = "Produtos em estoque:\n" + "\n".join(produtos)
        messagebox.showinfo("Lista de Produtos", mensagem)

# Criar a instância do sistema
sistema = Gestao("estoque.db")

# Criar a instância da interface e iniciar o loop principal
interface = InterfaceGestao(sistema)
interface.mainloop()
