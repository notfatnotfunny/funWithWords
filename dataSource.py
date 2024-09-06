import requests
from bs4 import BeautifulSoup
import numpy as np
import json
import stressFinder as sf

alfabeto = 'abcdefghijklmnopqrstuvwxyz'
alfa = []
for i in alfabeto:
    for j in alfabeto:
        for k in  alfabeto:
            alfa.append(i+j+k)
index = alfa.index('spr')
f = open('data.txt', 'w')
g = open('dataset.txt', 'w')

def listaParole():
    res = []
    for prefix in alfa:
        url = 'https://www.dizy.com/it/alfa/' + prefix + '?p=1'
        soup = BeautifulSoup(requests.get(url).content, 'html.parser')
        notFound = str(soup).split()
        if notFound[0] == 'Pagina' and notFound[1]=='Non':
            continue
        for p in range(12)[1:]:
            page = '?p=' + str(p)
            url = 'https://www.dizy.com/it/alfa/' + prefix + page
            print(url)
            response = requests.get(url)
            content = response.content
            soup = BeautifulSoup(content, 'html.parser')
            script_tag = str(soup.find('div', id = 'container')).split()
            if 'vuota.</i><br/>Vai' in script_tag:
                break
            for e in script_tag:
                if e[:15] == 'href="/it/voce/':
                    word = e.split('>')[1].split('<')[0]
                    print(word)
                    f.write(word + '\n')
                    res.append(word)
                    accWord = sf.fetchURL(word)
                    if accWord:
                        g.write(word + ',' + accWord + '\n') 
    return res

listaParole()