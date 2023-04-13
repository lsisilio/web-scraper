import requests
from bs4 import BeautifulSoup
import re
import pandas as pd
import math

url = 'https://www.kabum.com.br/livros/livros-de-historia-e-geografia'
headers = {'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36"}
site = requests.get(url, headers=headers)
soup = BeautifulSoup(site.content, 'html.parser')

#pegando a quantidade total de itens e separando apenas os números
qtd_itens = soup.find('div', id='listingCount').get_text().strip()
index = qtd_itens.find(' ')
qtd = qtd_itens[:index]
#Dicionario dos produtos
dic_produtos = {'nome':[], 'preco':[]}
#Dividindo o n de itens pelo n de itens/pag pra chegar no n de pag
ultima_pagina = math.ceil(int(qtd)/20)

for i in range(1, ultima_pagina+1):
    url_pag = f'https://www.kabum.com.br/livros/livros-de-historia-e-geografia?page_number={i}&page_size=20&facet_filters=&sort=most_searched'
    site = requests.get(url_pag, headers=headers)
    soup = BeautifulSoup(site.content, 'html.parser')
    produtos = soup.find_all('div', class_=re.compile('productCard'))

    for produto in produtos:
        nome = produto.find('span', class_=re.compile('nameCard')).get_text().strip()
        preco = produto.find('span', class_=re.compile('priceCard')).get_text().strip()

        dic_produtos['nome'].append(nome)
        dic_produtos['preco'].append(preco)

df = pd.DataFrame(dic_produtos)
print(dir)
df.to_csv('scraper_results.csv', encoding='utf-8', sep=';')
print("Success!")