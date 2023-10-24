tab = ["","",""]

print("Bonjour, comment vous appelez vous : ")
nom = input("Entrer votre nom : ")
prénom = input("Entrer votre prénom : " )
age = input("Quel age avez-vous ? : ")
taille = input("Votre taille en centimètre ? : ")
print("3 de vos fruits preferer : ")
for i in range(3):
    tab[i] = input("fruit : ")

personne = {"Nom":nom,"Prenom":prénom,"age":age,"taille":taille,"fruits":tab}
print("Voila ce que j'ai retenue :")
print(personne)