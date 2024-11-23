import tkinter as tk
from tkinter import filedialog, messagebox

# Função principal do editor de texto
def main():
    # Criar a janela principal
    root = tk.Tk()
    root.title("Editor de Texto Binário")
    root.geometry("800x600")  # Definir tamanho da janela

    # Criar o widget de texto onde o usuário poderá digitar
    text_area = tk.Text(root, wrap="none", undo=True)
    text_area.pack(fill=tk.BOTH, expand=True)

    # Função para abrir ficheiro binário
    def abrir_ficheiro():
        caminho = filedialog.askopenfilename(
            title="Abrir Ficheiro Binário",
            filetypes=[("Ficheiros Binários", "*.bin"), ("Todos os Ficheiros", "*.*")]
        )
        if caminho:
            try:
                with open(caminho, "rb") as f:
                    conteudo = f.read().decode("utf-8")
                    text_area.delete("1.0", tk.END)
                    text_area.insert(tk.END, conteudo)
            except Exception as e:
                messagebox.showerror("Erro", f"Não foi possível abrir o ficheiro: {e}")

    # Função para salvar o conteúdo no formato binário
    def salvar_ficheiro():
        caminho = filedialog.asksaveasfilename(
            title="Salvar Ficheiro Binário",
            defaultextension=".bin",
            filetypes=[("Ficheiros Binários", "*.bin"), ("Todos os Ficheiros", "*.*")]
        )
        if caminho:
            try:
                conteudo = text_area.get("1.0", tk.END).encode("utf-8")
                with open(caminho, "wb") as f:
                    f.write(conteudo)
                messagebox.showinfo("Sucesso", "Ficheiro salvo com sucesso!")
            except Exception as e:
                messagebox.showerror("Erro", f"Não foi possível salvar o ficheiro: {e}")

    # Função para sair do programa
    def sair():
        if messagebox.askyesno("Sair", "Tem a certeza que deseja sair?"):
            root.destroy()

    # Criar uma barra de menu
    menu_bar = tk.Menu(root)
    root.config(menu=menu_bar)

    # Adicionar menus (Ficheiro e Ajuda)
    menu_ficheiro = tk.Menu(menu_bar, tearoff=0)
    menu_ficheiro.add_command(label="Abrir", command=abrir_ficheiro)
    menu_ficheiro.add_command(label="Salvar", command=salvar_ficheiro)
    menu_ficheiro.add_separator()
    menu_ficheiro.add_command(label="Sair", command=sair)
    menu_bar.add_cascade(label="Ficheiro", menu=menu_ficheiro)

    menu_ajuda = tk.Menu(menu_bar, tearoff=0)
    menu_ajuda.add_command(
        label="Sobre",
        command=lambda: messagebox.showinfo("Sobre", "Editor de Texto Binário v1.0\nFeito com Python e Tkinter."),
    )
    menu_bar.add_cascade(label="Ajuda", menu=menu_ajuda)

    # Ligar o rato para selecionar texto
    text_area.bind("<Button-1>", lambda event: text_area.focus_set())

    # Ligar atalhos de teclado
    root.bind("<Control-s>", lambda event: salvar_ficheiro())
    root.bind("<Control-o>", lambda event: abrir_ficheiro())
    root.bind("<Control-q>", lambda event: sair())

    # Iniciar o loop principal da aplicação
    root.mainloop()


if __name__ == "__main__":
    main()
