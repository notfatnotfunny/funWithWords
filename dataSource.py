import requests
from bs4 import BeautifulSoup
import numpy as np
import json

alfabeto = 'abcdefghijklmnopqrstuvwxyz'
alfa = []
for i in alfabeto:
    for j in alfabeto:
        for k in  alfabeto:
            alfa.append(i+j+k)


def listaParole():
    res = []
    prefx = 'sor?p=15'
    url = 'https://www.dizy.com/it/alfa/' + prefx
    response = requests.get(url)
    content = response.content
    soup = BeautifulSoup(content, 'html.parser')
    script_tag = str(soup.find('div', id = 'container')).split()
    for e in script_tag:
        if e[:15] == 'href="/it/voce/':
            res.append(e.split('>')[1].split('<')[0])
    return res
print(listaParole())
