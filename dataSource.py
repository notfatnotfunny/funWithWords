import requests
from bs4 import BeautifulSoup
import numpy as np


alfabeto = 'abcdefghijklmnopqrstuvwxyz'
alfa = []
for i in alfabeto:
    for j in alfabeto:
        for k in  alfabeto:
            alfa.append(i+j+k)


def listaParole():
    res = []
    prefx = 'sor?p=1'
    url = 'https://www.dizy.com/it/alfa/' + prefx
    response = requests.get(url)
    content = response.content
    soup = BeautifulSoup(content, 'html.parser')
    script_tag = soup.find('div', id = 'container')
    
    return res
print(listaParole())