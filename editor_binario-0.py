import tkinter as tk
from tkinter import filedialog, messagebox

# Função principal do editor de texto
def main():
    # Criar a janela principal
    root = tk.Tk()
    root.title("Editor de Texto - TXT e BIN")
    root.geometry("800x600")  # Dimensão da janela

    # Criar widget de texto
    text_area = tk.Text(root, wrap="word", undo=True, font=("Arial", 12))
    text_area.pack(fill=tk.BOTH, expand=True)

    # Função para abrir ficheiros
    def abrir_ficheiro():
        caminho = filedialog.askopenfilename(
            title="Abrir Ficheiro",
            filetypes=[("Ficheiros TXT", "*.txt"), ("Ficheiros Binários", "*.bin"), ("Todos os Ficheiros", "*.*")]
        )
        if caminho:
            try:
                modo = "r" if caminho.endswith(".txt") else "rb"
                with open(caminho, modo) as f:
                    conteudo = f.read()
                    if modo == "rb":  # Decodificar se for binário
                        conteudo = conteudo.decode("utf-8")
                    text_area.delete("1.0", tk.END)
                    text_area.insert(tk.END, conteudo)
            except Exception as e:
                messagebox.showerror("Erro", f"Não foi possível abrir o ficheiro: {e}")

    # Função para salvar ficheiros
    def salvar_ficheiro():
        caminho = filedialog.asksaveasfilename(
            title="Salvar Ficheiro",
            defaultextension=".txt",
            filetypes=[("Ficheiros TXT", "*.txt"), ("Ficheiros Binários", "*.bin"), ("Todos os Ficheiros", "*.*")]
        )
        if caminho:
            try:
                conteudo = text_area.get("1.0", tk.END)
                modo = "w" if caminho.endswith(".txt") else "wb"
                with open(caminho, modo) as f:
                    if modo == "wb":
                        conteudo = conteudo.encode("utf-8")
                    f.write(conteudo)
                messagebox.showinfo("Sucesso", "Ficheiro salvo com sucesso!")
            except Exception as e:
                messagebox.showerror("Erro", f"Não foi possível salvar o ficheiro: {e}")

    # Função para criar novo ficheiro
    def novo_ficheiro():
        if messagebox.askyesno("Novo Ficheiro", "Deseja limpar o conteúdo atual?"):
            text_area.delete("1.0", tk.END)

    # Função para apagar texto selecionado
    def apagar_texto():
        try:
            text_area.delete(tk.SEL_FIRST, tk.SEL_LAST)
        except tk.TclError:
            messagebox.showwarning("Atenção", "Nenhum texto selecionado para apagar.")

    # Função para sublinhar texto selecionado
    def sublinhar_texto():
        try:
            start = text_area.index(tk.SEL_FIRST)
            end = text_area.index(tk.SEL_LAST)
            text_area.tag_add("sublinhado", start, end)
            text_area.tag_config("sublinhado", underline=True)
        except tk.TclError:
            messagebox.showwarning("Atenção", "Nenhum texto selecionado para sublinhar.")

    # Função para sair do programa
    def sair():
        if messagebox.askyesno("Sair", "Tem a certeza que deseja sair?"):
            root.destroy()

    # Adicionar atalhos de teclado
    root.bind("<Control-o>", lambda event: abrir_ficheiro())
    root.bind("<Control-s>", lambda event: salvar_ficheiro())
    root.bind("<Control-n>", lambda event: novo_ficheiro())
    root.bind("<Control-q>", lambda event: sair())
    root.bind("<Control-u>", lambda event: sublinhar_texto())

    # Criar barra de menu
    menu_bar = tk.Menu(root)
    root.config(menu=menu_bar)

    # Menu "Ficheiro"
    menu_ficheiro = tk.Menu(menu_bar, tearoff=0)
    menu_ficheiro.add_command(label="Novo", command=novo_ficheiro, accelerator="Ctrl+N")
    menu_ficheiro.add_command(label="Abrir", command=abrir_ficheiro, accelerator="Ctrl+O")
    menu_ficheiro.add_command(label="Salvar", command=salvar_ficheiro, accelerator="Ctrl+S")
    menu_ficheiro.add_separator()
    menu_ficheiro.add_command(label="Sair", command=sair, accelerator="Ctrl+Q")
    menu_bar.add_cascade(label="Ficheiro", menu=menu_ficheiro)

    # Menu "Editar"
    menu_editar = tk.Menu(menu_bar, tearoff=0)
    menu_editar.add_command(label="Apagar Seleção", command=apagar_texto)
    menu_editar.add_command(label="Sublinhar Seleção", command=sublinhar_texto, accelerator="Ctrl+U")
    menu_bar.add_cascade(label="Editar", menu=menu_editar)

    # Menu "Ajuda"
    menu_ajuda = tk.Menu(menu_bar, tearoff=0)
    menu_ajuda.add_command(
        label="Sobre", command=lambda: messagebox.showinfo("Sobre", "Editor de Texto Avançado v1.0\nCriado em Python.")
    )
    menu_bar.add_cascade(label="Ajuda", menu=menu_ajuda)

    # Iniciar o loop principal
    root.mainloop()


if __name__ == "__main__":
    main()
