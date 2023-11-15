import requests
from bs4 import BeautifulSoup
import csv
import pandas as pd
import matplotlib.pyplot as plt

def find_string(main_string, sub_string):
    return sub_string in main_string

def scrape_page(soup, revs):
    # recupere tous les éléments <div> HTML de la page
    rev_elements = soup.find_all('div', class_='feed-post-card-vs feed-card flex flex-column sl-post sl-feed-card js-card js-page-num-')

    # itération sur les elements de la liste
    # pour extraire les informations
    # par offre
    for rev_element in rev_elements:
        # Extrait le nom de l'offre
        nom_element = rev_element.find('h6', class_='card-title sl-card-title')
        nom_rev = nom_element.find('a', href=True).text
        if find_string(nom_rev,"Honda") == True :
            # Extrait le time stamp
            timestamp = rev_element.find('span', class_='timestamp flex flex-align-center nowrap').text

            revs.append(
                {
                    'Nom': nom_rev,
                    'Time': timestamp,
                }
            )

# url du site 
base_url = 'https://www.motorcycle.com'

# endpoint url
page_url = '/manufacturer/reviews.html?'


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
    reviews = []

    # scrape la première page
    scrape_page(soup, reviews)

    # Recupere l'element html next
    next_page_link = soup.find('a', class_='sl-next-page')

    i=0

    # Si il y a une autre page a scrape ou compteur
    while next_page_link is not None and i<3:
        next_page_url = next_page_link['href']

        # recupe la page suivante
        page = requests.get(base_url + next_page_url, headers=headers)

        # parse cette dernière
        soup = BeautifulSoup(page.text, 'html.parser')

        # scrape
        scrape_page(soup, reviews)

        # rebelotte, on cherche l'element next
        next_page_link = soup.find('a', class_='sl-next-page')

        # On fait monter le compteur
        print("page scrapper numéro : "+str(i))
        i+=1

    # lecture de "offre.csv" ou création si non présent
    csv_file = open('review_moto.csv', 'w', encoding='utf-8', newline='')

    # initialize le writer
    writer = csv.writer(csv_file)

    # Ecriture avec colonne
    writer.writerow(['Nom', 'Time'])

    # Ecriture a partir du dico offre
    for rev in reviews:
        writer.writerow(rev.values())

    # Fin de l'ecriture
    csv_file.close()        

    # Analyse du fichier creer
    df = pd.read_csv ('review_moto.csv')
    print(df)

    # Affichage des stats
    print(df.describe())

    
    