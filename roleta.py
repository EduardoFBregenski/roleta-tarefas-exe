import tkinter as tk
from tkinter import ttk, messagebox
import random
import json
import os

ARQUIVO = "dados_roleta.json"

CATEGORIAS_PADRAO = {
    "Tarefas de casa": ["Lavar louça", "Varrer", "Tirar o lixo"],
    "Noite da qualidade": ["Filme", "Jogo", "Passeio", "Pizza + série"],
    "Tipo de refeição": ["Macarrão", "Hambúrguer", "Comida japonesa", "Salada"]
}

def carregar_dados():
    if os.path.exists(ARQUIVO):
        try:
            with open(ARQUIVO, "r", encoding="utf-8") as f:
                return json.load(f)
        except:
            return CATEGORIAS_PADRAO.copy()
    return CATEGORIAS_PADRAO.copy()

def salvar_dados():
    with open(ARQUIVO, "w", encoding="utf-8") as f:
        json.dump(dados, f, ensure_ascii=False, indent=2)

def atualizar_lista():
    categoria = aba_atual.get()
    lista.delete(0, tk.END)
    for item in dados[categoria]:
        lista.insert(tk.END, item)

def adicionar_item():
    categoria = aba_atual.get()
    texto = entrada.get().strip()
    if not texto:
        return
    dados[categoria].append(texto)
    entrada.delete(0, tk.END)
    salvar_dados()
    atualizar_lista()

def remover_item():
    categoria = aba_atual.get()
    sel = lista.curselection()
    if not sel:
        messagebox.showinfo("Aviso", "Selecione um item para remover.")
        return
    item = lista.get(sel[0])
    dados[categoria].remove(item)
    salvar_dados()
    atualizar_lista()

def girar_roleta():
    categoria = aba_atual.get()
    itens = dados[categoria]
    if not itens:
        messagebox.showinfo("Aviso", "Não há opções nessa categoria.")
        return
    escolhido = random.choice(itens)
    resultado.set(f"🎯 Sorteado: {escolhido}")

# --- App ---
dados = carregar_dados()

janela = tk.Tk()
janela.title("Roleta de Tarefas")
janela.geometry("520x420")

aba_atual = tk.StringVar(value=list(dados.keys())[0])
resultado = tk.StringVar(value="🎯 Sorteado: -")

frame_top = tk.Frame(janela)
frame_top.pack(pady=10)

tk.Label(frame_top, text="Categoria:", font=("Arial", 11)).pack(side=tk.LEFT, padx=5)

combo = ttk.Combobox(frame_top, textvariable=aba_atual, values=list(dados.keys()), state="readonly", width=25)
combo.pack(side=tk.LEFT)

def on_categoria_change(event=None):
    resultado.set("🎯 Sorteado: -")
    atualizar_lista()

combo.bind("<<ComboboxSelected>>", on_categoria_change)

frame_add = tk.Frame(janela)
frame_add.pack(pady=10)

entrada = tk.Entry(frame_add, width=35)
entrada.pack(side=tk.LEFT, padx=5)

btn_add = tk.Button(frame_add, text="Adicionar", command=adicionar_item)
btn_add.pack(side=tk.LEFT)

lista = tk.Listbox(janela, width=60, height=12)
lista.pack(pady=10)

frame_btns = tk.Frame(janela)
frame_btns.pack(pady=5)

tk.Button(frame_btns, text="🗑 Remover selecionado", command=remover_item).pack(side=tk.LEFT, padx=5)
tk.Button(frame_btns, text="🎡 Girar roleta", command=girar_roleta).pack(side=tk.LEFT, padx=5)

tk.Label(janela, textvariable=resultado, font=("Arial", 14, "bold")).pack(pady=15)

atualizar_lista()
janela.mainloop()
