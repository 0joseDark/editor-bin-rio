import tkinter as tk
from tkinter import filedialog, messagebox
import os
import subprocess


class FileEditorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Editor de Ficheiros Avançado")
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

        # Secção de leitura de memória
        memory_frame = tk.Frame(self.root)
        memory_frame.pack(fill="x")

        tk.Label(memory_frame, text="Endereço Inicial:").pack(side="left", padx=5)
        self.start_address_entry = tk.Entry(memory_frame, width=10)
        self.start_address_entry.pack(side="left")

        tk.Label(memory_frame, text="Endereço Final:").pack(side="left", padx=5)
        self.end_address_entry = tk.Entry(memory_frame, width=10)
        self.end_address_entry.pack(side="left")

        tk.Button(memory_frame, text="Ler Memória", command=self.read_memory).pack(side="left", padx=5)

    def new_file(self):
        """Cria um novo ficheiro."""
        self.file_path = None
        self.text_area.delete(1.0, tk.END)

    def open_file(self):
        """Abre um ficheiro."""
        self.file_path = filedialog.askopenfilename(
            filetypes=[("Todos os Ficheiros", "*.*"),
                       ("Textos", "*.txt"),
                       ("Markdown", "*.md"),
                       ("Binários", "*.bin")])
        if self.file_path:
            with open(self.file_path, 'rb') as file:
                content = file.read()
            self.text_area.delete(1.0, tk.END)
            try:
                self.text_area.insert(1.0, content.decode())
            except UnicodeDecodeError:
                messagebox.showwarning("Aviso", "Exibindo ficheiro binário como texto.")
                self.text_area.insert(1.0, content.hex())

    def save_file(self):
        """Guarda o ficheiro."""
        if not self.file_path:
            self.save_as()
        else:
            self._write_to_file()

    def save_as(self):
        """Guarda o ficheiro com outro nome."""
        self.file_path = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Textos", "*.txt"), ("Markdown", "*.md"), ("Binários", "*.bin")])
        if self.file_path:
            self._write_to_file()

    def _write_to_file(self):
        """Escreve no ficheiro o conteúdo do editor."""
        try:
            content = self.text_area.get(1.0, tk.END).strip()
            if self.file_path.endswith(".bin"):
                content = bytes.fromhex(content)
            with open(self.file_path, 'wb') as file:
                file.write(content.encode() if isinstance(content, str) else content)
            messagebox.showinfo("Info", "Ficheiro guardado com sucesso!")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao guardar ficheiro: {e}")

    def delete_file(self):
        """Apaga o ficheiro atual."""
        if self.file_path and os.path.exists(self.file_path):
            os.remove(self.file_path)
            messagebox.showinfo("Info", "Ficheiro apagado com sucesso!")
            self.new_file()
        else:
            messagebox.showerror("Erro", "Ficheiro não encontrado!")

    def run_file(self):
        """Executa o ficheiro atual."""
        if self.file_path:
            try:
                subprocess.run(self.file_path, check=True, shell=True)
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao executar ficheiro: {e}")

    def read_memory(self):
        """Lê secção de memória de um ficheiro binário."""
        if not self.file_path or not self.file_path.endswith(".bin"):
            messagebox.showerror("Erro", "Selecione um ficheiro binário válido!")
            return

        try:
            start = int(self.start_address_entry.get())
            end = int(self.end_address_entry.get())
            with open(self.file_path, 'rb') as file:
                file.seek(start)
                data = file.read(end - start)
            self.text_area.delete(1.0, tk.END)
            self.text_area.insert(1.0, data.hex())
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao ler memória: {e}")

    def exit_app(self):
        """Encerra a aplicação."""
        self.root.quit()


if __name__ == "__main__":
    root = tk.Tk()
    app = FileEditorApp(root)
    root.geometry("800x600")
    root.mainloop()
