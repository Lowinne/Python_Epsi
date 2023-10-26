import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import json
import phonenumbers

class Contact:
    def __init__(self,root):
        self.root = root
        self.root.title("Contact")

        # Variables des contacts
        self.contacts = []

        # Creation des widgets
        self.description_label = tk.Label(root, text="Contact")
        self.creation_label = tk.Label(root, text="Créer un contact")
        self.surname_label = tk.Label(root, text="Nom")
        self.surname_entry = tk.Entry(root, width=15)
        self.name_label = tk.Label(root, text="Prénom")
        self.name_entry = tk.Entry(root, width=15)
        self.tel_label = tk.Label(root, text="NoTel")
        self.tel_entry = tk.Entry(root, width=15)

        # Affichager les contacts dans un tableau
        self.tree = ttk.Treeview(root, columns=("ID", "Name", "Surname","Indicatif", "Tel"))

        self.tree.heading("ID", text="ID")
        self.tree.heading("Name", text="Prénom")
        self.tree.heading("Surname", text="Nom")
        self.tree.heading("Indicatif", text="Indicatif")
        self.tree.heading("Tel", text="Numéro")

        # Bouton d'action
        # Ajouter
        self.add_button = tk.Button(root, text="Ajouter le contact", command=self.add_contact)
        # Modifier
        self.update_button = tk.Button(root, text="Mettre à jour le contact", command=self.update_contact)
        # Supprimer
        self.rm_button = tk.Button(root, text="Supprimer le contact", command=self.delete_contact)
        # Export
        self.export_button = tk.Button(root, text="Exporter en json", command=self.export_to_json)
        # Plus d'info
        self.more_button = tk.Button(root, text="Plus d'information", command=self.more_info)
        # Charger json
        self.charger_boutton = tk.Button(root, text="Charger Json", command=self.laod_json)

        #.pack
        self.description_label.pack(pady=5)
        self.creation_label.pack(pady=5)
        self.surname_label.pack(pady=5)
        self.surname_entry.pack(pady=5)
        self.name_label.pack(pady=5)
        self.name_entry.pack(pady=5)
        self.tel_label.pack(pady=5)
        self.tel_entry.pack(pady=5)
        self.add_button.pack(pady=10)
        self.rm_button.pack(pady=10)
        self.update_button.pack(pady=10)
        self.export_button.pack(pady=10)
        self.more_button.pack(pady=10)
        self.charger_boutton.pack(pady=10)
        self.tree.pack(pady=10)


    # Ajouter un contact
    def add_contact(self):
        surname = self.surname_entry.get()
        name = self.name_entry.get()
        notelstr = self.tel_entry.get()
        # Test regex
        if surname and name:
            try:
                notel = phonenumbers.parse(notelstr)
            except ValueError:
                messagebox.showerror("Erreur","Format du numéro non reconnue.")
                return
            contact = {"surname": surname, "name": name, "Indicatif":notel.country_code ,"NoTel": notel.national_number}
            self.contacts.append(contact)
            #update
            self.update_treeview()
            #clear
            self.clear_entry()
    
    def update_treeview(self):

        # Clear le tableau
        for item in self.tree.get_children():
            self.tree.delete(item)

        #Re peuplage
        for i, contact in enumerate(self.contacts, start=1):
            #Tuple
            values = (i,contact["surname"],contact["name"],contact["Indicatif"],contact["NoTel"])
            iid = self.tree.insert("", "end", values=values)

    def clear_entry(self):
        self.surname_entry.delete(0, tk.END)
        self.name_entry.delete(0, tk.END)
        self.tel_entry.delete(0, tk.END)

    def delete_contact(self):
        selected_item = self.tree.selection()
        if selected_item:
            index = int(self.tree.item(selected_item, "values")[0]) - 1
            del self.contacts[index]
            self.update_treeview()    
    
    def update_contact(self):
        selected_item = self.tree.selection()
        if selected_item:
            index = int(self.tree.item(selected_item, "values")[0]) - 1
            if self.surname_entry.get():
                contactt = self.contacts[index]
                contactt["surname"] = self.surname_entry.get()
                self.update_treeview()
            if self.name_entry.get():
                contactt = self.contacts[index]
                contactt["name"] = self.name_entry.get()
                self.update_treeview()
            if self.tel_entry.get():
                contactt = self.contacts[index]
                contactt["NoTel"] = self.tel_entry.get()
                self.update_treeview()

    def export_to_json(self):
        file_path = tk.filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON files", "*.json"), ("All files", "*.*")])
        if file_path:
            with open(file_path, "w") as file:
                json.dump(self.contacts, file, indent=2)
            messagebox.showinfo("Export Successful", f"Tasks exported to {file_path}")

    def laod_json(self):
        file_path = tk.filedialog.askopenfilename(defaultextension=".json", filetypes=[("JSON files", "*.json"), ("All files", "*.*")])
        try:
            with open(file_path, "r") as fichier:
                self.contacts = json.load(fichier)  #Charger la liste des listes enregistrées
        except FileNotFoundError:
            self.contacts = []  #Si le fichier n'existe pas, initialiser une liste vide
        self.update_treeview()
        
    def more_info(self):
        selected_item = self.tree.selection()
        if selected_item:
            index = int(self.tree.item(selected_item, "values")[0]) - 1
            contactt = self.contacts[index]
            messagebox.showinfo("Informations","Prénom : "+contactt["surname"]+" Nom : "+contactt["name"]+" Numéro : +"+str(contactt["Indicatif"])+str(contactt["NoTel"]))
            
if __name__ == "__main__":
    root = tk.Tk()
    app = Contact(root)
    root.mainloop()