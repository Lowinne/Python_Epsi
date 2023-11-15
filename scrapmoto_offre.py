import requests
from bs4 import BeautifulSoup
import csv
import pandas as pd
import matplotlib.pyplot as plt

def scrape_page(soup, offres):
    # recupere tous les éléments <div> HTML de la page
    offre_elements = soup.find_all('div', class_='Vehiculecard_Vehiculecard_cardBody')

    # itération sur les elements de la liste
    # pour extraire les informations
    # par offre
    for offre_element in offre_elements:
        # Extrait le nom de l'offre
        modele = offre_element.find('h2', class_='Text_Text_text Vehiculecard_Vehiculecard_title Text_Text_subtitle2').text
        # Extrait le prix de l'offre
        prix = offre_element.find('span', class_='Text_Text_text Vehiculecard_Vehiculecard_price Text_Text_subtitle2').text
        prix_temp = prix.replace(" €", "")
        # Extrait le CC de l'offre
        cc = offre_element.find('div', class_='Text_Text_text Vehiculecard_Vehiculecard_subTitle Text_Text_body2').text
        # Extrait l'année de l'offre
        ann = offre_element.find('div', class_='Text_Text_text Vehiculecard_Vehiculecard_characteristicsItems Text_Text_body2').text
        offres.append(
            {
                'Modele': modele,
                'prix': prix_temp.replace(" ", ""),
                'Cylindre': cc,
                'Année': ann
            }
        )

# url du site 
base_url = 'https://www.lacentrale.fr'

#url de la page
page_url = '/occasion-moto-marque-honda.html'

# definition du user-agent pour se faire passer pour un navigateur
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'fr,fr-FR;q=0.8,en-US;q=0.5,en;q=0.3'
}

# recuperation de la page
page = requests.get(base_url + page_url, headers=headers)

if(page.status_code==200):
    # parsage de la page avec bs4
    soup = BeautifulSoup(page.text, 'html.parser')

    # Initialise la variable contenant les offres
    offres = []

    # scrape la première page
    scrape_page(soup, offres)

    # Recupere l'element html next
    next_page_link = soup.find('a', attrs={"aria-label": "next-page"})

    i=0

    # Si il y a une autre page a scrape ou compteur
    while next_page_link is not None and i<10:
        next_page_url = next_page_link['href']

        # recupe la page suivante
        page = requests.get(base_url + next_page_url, headers=headers)

        # parse cette dernière
        soup = BeautifulSoup(page.text, 'html.parser')

        # scrape
        scrape_page(soup, offres)

        # rebelotte, on cherche l'element next
        next_page_link = soup.find('a', attrs={"aria-label": "next-page"})

        # On fait monter le compteur
        print("page scrapper numéro : "+str(i))
        i+=1

    # lecture de "offre.csv" ou création si non présent
    csv_file = open('offres_moto.csv', 'w', encoding='utf-8', newline='')

    # initialize le writer
    writer = csv.writer(csv_file)

    # Ecriture avec colonne
    writer.writerow(['Modele', 'prix', 'Cylindre','Année'])

    # Ecriture a partir du dico offre
    for offre in offres:
        writer.writerow(offre.values())

    # Fin de l'ecriture
    csv_file.close()        

    # Analyse du fichier creer
    df = pd.read_csv ('offres_moto.csv')
    print(df.head())

    # Affichage des stats
    print(df.describe())

    # Filtrage des données par année
    filtered_data = df[df['Année'] > 2021]
    print(filtered_data)

    # Création de l'histogramme
    df['prix'].plot(kind='hist', bins=20, edgecolor='black')
    plt.title('Distribution des prix')
    plt.xlabel('Prix')
    plt.ylabel('Fréquence')
    plt.show()
    


    


    



