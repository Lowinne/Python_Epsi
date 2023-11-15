import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import json
from datetime import datetime

class GestionnaireTache:
    def __init__(self, root):
        self.root = root
        self.root.title("Gestionnaire de tache")

        # Variable des taches
        self.tasks = []

        # Creation des widgets
        self.description_label = tk.Label(root, text="Description:")
        self.description_entry = tk.Entry(root, width=30)
        self.date_label = tk.Label(root, text="Date (YYYY-MM-DD):")
        self.date_entry = tk.Entry(root, width=15)
        self.add_button = tk.Button(root, text="Ajouter", command=self.add_task)

        # Treeview pour afficher dans un tableau
        self.tree = ttk.Treeview(root, columns=("ID", "Description", "Due Date", "Status"))
        
        self.tree.heading("ID", text="ID")
        self.tree.heading("Description", text="Description")
        self.tree.heading("Due Date", text="Date")
        self.tree.heading("Status", text="Statut")

        # Boutton d'action
        self.mark_done_button = tk.Button(root, text="Marque comme fait", command=self.done)
        self.delete_button = tk.Button(root, text="Supprimer", command=self.delete)

        # Boutton pour generer le Json
        self.export_button = tk.Button(root, text="Exporter en Json", command=self.export_to_json)

        # .pack
        self.description_label.pack(pady=5)
        self.description_entry.pack(pady=5)
        self.date_label.pack(pady=5)
        self.date_entry.pack(pady=5)
        self.add_button.pack(pady=10)
        self.tree.pack(pady=10)
        self.mark_done_button.pack(pady=5)
        self.delete_button.pack(pady=5)
        self.export_button.pack(pady=10)

    def add_task(self):
        description = self.description_entry.get()
        date_str = self.date_entry.get()
        #test reg ex
        if description and date_str:
            try:
                due_date = datetime.strptime(date_str, "%Y-%m-%d").strftime("%Y-%m-%d")
            except ValueError:
                messagebox.showerror("Erreur", "format de date invalide, YYYY-MM-DD.")
                return

            task = {"description": description, "due_date": due_date, "status": "Not Done"}
            self.tasks.append(task)
            self.update_treeview()
            self.clear()

    def update_treeview(self):
        # Trier les tache par date
        self.tasks.sort(key=lambda x: datetime.strptime(x["due_date"], "%Y-%m-%d"))

        # Clear les taches
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Reintégration des taches dans le tableau
        for i, task in enumerate(self.tasks, start=1):
            #tuple
            values = (i, task["description"], task["due_date"], task.get("status", "Not Done"))
            iid = self.tree.insert("", "end", values=values)
            # Changer la couleur en fonction du statut
            if task.get("status") == "Done":
                self.tree.tag_configure('done', background='#009000')
                self.tree.item(iid, tags=('done',))

    def clear(self):
        self.description_entry.delete(0, tk.END)
        self.date_entry.delete(0, tk.END)

    def done(self):
        selected_item = self.tree.selection()
        if selected_item:
            index = int(self.tree.item(selected_item, "values")[0]) - 1
            self.tasks[index]["status"] = "Done"
            self.update_treeview()

    def delete(self):
        selected_item = self.tree.selection()
        if selected_item:
            index = int(self.tree.item(selected_item, "values")[0]) - 1
            del self.tasks[index]
            self.update_treeview()

    def export_to_json(self):
        file_path = tk.filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON files", "*.json"), ("All files", "*.*")])
        if file_path:
            with open(file_path, "w") as file:
                json.dump(self.tasks, file, indent=2)
            messagebox.showinfo("Export Successful", f"Tasks exported to {file_path}")

if __name__ == "__main__":
    root = tk.Tk()
    app = GestionnaireTache(root)
    root.mainloop()
