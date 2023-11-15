import requests
from bs4 import BeautifulSoup


base_url = "https://quotes.toscrape.com/"
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36'
}
# scraping one page
try:
    page = requests.get(base_url,headers=headers)
except:
    print("L'appel HTTP a échoué")


# premiere page
if(page.status_code==200):
    print("ok")
    soup = BeautifulSoup(page.text, 'html.parser')
    quotes = []
    quote_elements = soup.find_all('div', class_='quote')

    for quote_element in quote_elements:
        # extract the text of the quote
        text = quote_element.find('span', class_='text').text
        # extract the author of the quote
        author = quote_element.find('small', class_='author').text

        # extract the tag <a> HTML elements related to the quote
        tag_elements = quote_element.select('.tags .tag')

        # store the list of tag strings in a list
        tags = []
        for tag_element in tag_elements:
            tags.append(tag_element.text)
        
        quotes.append(
        {
            'text': text,
            'author': author,
            'tags': ', '.join(tags) # merge the tags into a "A, B, ..., Z" string
        })

    # boucle next page
    # get the "Next →" HTML element
    next_li_element = soup.find('li', class_='next')

    # if there is a next page to scrape
    while next_li_element is not None:
        next_page_relative_url = next_li_element.find('a', href=True)['href']

        # get the new page
        page = requests.get(base_url + next_page_relative_url, headers=headers)

        # parse the new page
        soup = BeautifulSoup(page.text, 'html.parser')
        for quote_element in quote_elements:
            # extract the text of the quote
            text = quote_element.find('span', class_='text').text
            # extract the author of the quote
            author = quote_element.find('small', class_='author').text

            # extract the tag <a> HTML elements related to the quote
            tag_elements = quote_element.select('.tags .tag')

            # store the list of tag strings in a list
            tags = []
            for tag_element in tag_elements:
                tags.append(tag_element.text)
            
            quotes.append(
            {
                'text': text,
                'author': author,
                'tags': ', '.join(tags) # merge the tags into a "A, B, ..., Z" string
            })

        quote_elements = soup.find_all('div', class_='quote')

        # look for the "Next →" HTML element in the new page
        next_li_element = soup.find('li', class_='next')


    print(quotes)

    

