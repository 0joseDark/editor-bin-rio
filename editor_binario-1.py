import tkinter as tk
from tkinter import filedialog, messagebox
import os
import subprocess


class FileEditorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Editor de Ficheiros")
        self.file_path = None

        # Criar menu
        menu = tk.Menu(self.root)
        self.root.config(menu=menu)

        # Submenus
        file_menu = tk.Menu(menu, tearoff=0)
        menu.add_cascade(label="Ficheiro", menu=file_menu)
        file_menu.add_command(label="Novo", command=self.new_file)
        file_menu.add_command(label="Abrir", command=self.open_file)
        file_menu.add_command(label="Guardar", command=self.save_file)
        file_menu.add_command(label="Guardar Como", command=self.save_as)
        file_menu.add_command(label="Apagar", command=self.delete_file)
        file_menu.add_separator()
        file_menu.add_command(label="Sair", command=self.exit_app)

        run_menu = tk.Menu(menu, tearoff=0)
        menu.add_cascade(label="Executar", menu=run_menu)
        run_menu.add_command(label="Correr Ficheiro", command=self.run_file)

        # Área de texto
        self.text_area = tk.Text(self.root, wrap="word", font=("Courier New", 12))
        self.text_area.pack(expand=1, fill="both")

    def new_file(self):
        """Limpa a área de texto para criar um novo ficheiro."""
        self.file_path = None
        self.text_area.delete(1.0, tk.END)

    def open_file(self):
        """Abre um ficheiro existente."""
        self.file_path = filedialog.askopenfilename(
            filetypes=[("Todos os Ficheiros", "*.*"),
                       ("Textos", "*.txt"),
                       ("Markdown", "*.md"),
                       ("Binários", "*.bin")])
        if self.file_path:
            try:
                with open(self.file_path, 'rb') as file:
                    content = file.read()
                self.text_area.delete(1.0, tk.END)
                try:
                    self.text_area.insert(1.0, content.decode())
                except UnicodeDecodeError:
                    self.text_area.insert(1.0, content)
            except Exception as e:
                messagebox.showerror("Erro", f"Não foi possível abrir o ficheiro: {e}")

    def save_file(self):
        """Guarda o ficheiro atual."""
        if not self.file_path:
            self.save_as()
        else:
            try:
                with open(self.file_path, 'w') as file:
                    file.write(self.text_area.get(1.0, tk.END).strip())
                messagebox.showinfo("Info", "Ficheiro guardado com sucesso!")
            except Exception as e:
                messagebox.showerror("Erro", f"Não foi possível guardar o ficheiro: {e}")

    def save_as(self):
        """Guarda o ficheiro com um novo nome."""
        self.file_path = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Textos", "*.txt"), ("Markdown", "*.md"), ("Binários", "*.bin")])
        if self.file_path:
            self.save_file()

    def delete_file(self):
        """Apaga o ficheiro atual."""
        if self.file_path and os.path.exists(self.file_path):
            try:
                os.remove(self.file_path)
                messagebox.showinfo("Info", "Ficheiro apagado com sucesso!")
                self.new_file()
            except Exception as e:
                messagebox.showerror("Erro", f"Não foi possível apagar o ficheiro: {e}")
        else:
            messagebox.showerror("Erro", "Nenhum ficheiro selecionado ou ficheiro não existe!")

    def run_file(self):
        """Executa o ficheiro selecionado."""
        if self.file_path:
            try:
                if self.file_path.endswith('.bin'):
                    subprocess.run(self.file_path, check=True)
                else:
                    os.startfile(self.file_path)
            except Exception as e:
                messagebox.showerror("Erro", f"Não foi possível executar o ficheiro: {e}")
        else:
            messagebox.showerror("Erro", "Nenhum ficheiro selecionado para executar!")

    def exit_app(self):
        """Encerra a aplicação."""
        self.root.quit()


if __name__ == "__main__":
    root = tk.Tk()
    app = FileEditorApp(root)
    root.geometry("800x600")  # Define o tamanho inicial da janela
    root.mainloop()
