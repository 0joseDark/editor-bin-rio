import os  # Para manipular ficheiros e pastas
import struct  # Para leitura e escrita de ficheiros binários
import psutil  # Para ler memória, CPU e dispositivos conectados
import tkinter as tk  # Interface gráfica
from tkinter import filedialog, messagebox

# Função para criar ficheiros
def criar_ficheiro():
    caminho = filedialog.asksaveasfilename(defaultextension=".txt", 
                                           filetypes=[("Texto", "*.txt"), 
                                                      ("Markdown", "*.md"), 
                                                      ("Binário", "*.bin")])
    if caminho:
        with open(caminho, 'w') as f:
            f.write("")  # Cria um ficheiro vazio
        messagebox.showinfo("Criado", f"Ficheiro criado: {caminho}")

# Função para abrir ficheiros
def abrir_ficheiro():
    caminho = filedialog.askopenfilename(filetypes=[("Todos os Ficheiros", "*.*")])
    if caminho:
        modo = 'rb' if caminho.endswith('.bin') else 'r'
        with open(caminho, modo) as f:
            conteudo = f.read()
        if modo == 'r':
            texto.insert("1.0", conteudo)
        else:
            texto.insert("1.0", conteudo.hex())
        global ficheiro_atual
        ficheiro_atual = caminho

# Função para guardar ficheiros
def guardar_ficheiro():
    global ficheiro_atual
    if ficheiro_atual:
        with open(ficheiro_atual, 'w') as f:
            f.write(texto.get("1.0", tk.END))
        messagebox.showinfo("Guardado", f"Ficheiro guardado: {ficheiro_atual}")
    else:
        guardar_como()

# Função para guardar ficheiros como
def guardar_como():
    caminho = filedialog.asksaveasfilename(defaultextension=".txt", 
                                           filetypes=[("Texto", "*.txt"), 
                                                      ("Markdown", "*.md"), 
                                                      ("Binário", "*.bin")])
    if caminho:
        with open(caminho, 'w') as f:
            f.write(texto.get("1.0", tk.END))
        global ficheiro_atual
        ficheiro_atual = caminho
        messagebox.showinfo("Guardado", f"Ficheiro guardado: {caminho}")

# Função para apagar ficheiros
def apagar_ficheiro():
    caminho = filedialog.askopenfilename()
    if caminho:
        os.remove(caminho)
        messagebox.showinfo("Apagado", f"Ficheiro apagado: {caminho}")

# Função para ler memória e registos
def ler_memoria():
    inicio = int(entrada_mem_inicio.get(), 16)
    fim = int(entrada_mem_fim.get(), 16)
    memoria = psutil.virtual_memory()
    messagebox.showinfo("Memória", f"Total: {memoria.total} Bytes\nUsada: {memoria.used} Bytes")

# Função para verificar portas USB
def verificar_usb():
    dispositivos = [d.device for d in psutil.disk_partitions() if 'usb' in d.opts]
    messagebox.showinfo("Portas USB", f"Dispositivos USB: {', '.join(dispositivos)}")

# Configuração da janela principal
janela = tk.Tk()
janela.title("Editor de Ficheiros e Varredura")
janela.geometry("600x400")

# Caixa de texto para edição
texto = tk.Text(janela, wrap="word", height=15)
texto.pack(fill="both", expand=True, padx=10, pady=10)

# Botões de ficheiros
tk.Button(janela, text="Criar Ficheiro", command=criar_ficheiro).pack(side="left", padx=5, pady=5)
tk.Button(janela, text="Abrir Ficheiro", command=abrir_ficheiro).pack(side="left", padx=5, pady=5)
tk.Button(janela, text="Guardar Ficheiro", command=guardar_ficheiro).pack(side="left", padx=5, pady=5)
tk.Button(janela, text="Guardar Como", command=guardar_como).pack(side="left", padx=5, pady=5)
tk.Button(janela, text="Apagar Ficheiro", command=apagar_ficheiro).pack(side="left", padx=5, pady=5)

# Campos para varredura de memória
tk.Label(janela, text="Endereço Início (Hex):").pack(pady=5)
entrada_mem_inicio = tk.Entry(janela)
entrada_mem_inicio.pack(pady=5)
tk.Label(janela, text="Endereço Fim (Hex):").pack(pady=5)
entrada_mem_fim = tk.Entry(janela)
entrada_mem_fim.pack(pady=5)
tk.Button(janela, text="Ler Memória", command=ler_memoria).pack(pady=5)

# Botão para portas USB
tk.Button(janela, text="Verificar USB", command=verificar_usb).pack(pady=5)

janela.mainloop()
