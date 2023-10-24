import tkinter as tk



def action_bouton():
    print("pseudo : "+champ_nom.get() + ", email : "+champ_email.get() +", mdp : "+champ_mdp.get())
    

fenetre = tk.Tk()
fenetre.title("Ma première interface graphique")

etiquette_inscription = tk.Label(fenetre, text="Inscription")
etiquette_pseudo = tk.Label(fenetre, text="Pseudo")
champ_nom = tk.Entry(fenetre)

etiquette_email = tk.Label(fenetre, text="Email")
champ_email = tk.Entry(fenetre)

etiquette_mdp = tk.Label(fenetre, text="Mot de passe")
champ_mdp = tk.Entry(fenetre)


bouton = tk.Button(fenetre, text="Cliquez", command=action_bouton)

etiquette_inscription.pack()
etiquette_pseudo.pack()
champ_nom.pack()

etiquette_email.pack()
champ_email.pack()

etiquette_mdp.pack()
champ_mdp.pack()

bouton.pack()

fenetre.geometry("400x300")

fenetre.mainloop()