import stressFinder as sf
import numpy as np

data = np.loadtxt("95000_parole_italiane_con_nomi_propri.txt", dtype=str, encoding='UTF-8')

def accent(string):
    bl = False
    for e in string:
        if e in 'éèàáìíòóùú':
            bl = True
            pass
    return bl

def accentazione(syllabWord):
    word = ''
    res = ['tronca', 'piana', 'sdrucciola', 'bisdrucciola']
    for i in range(len(syllabWord))[::-1]:
        if accent(syllabWord[i]):
            word = res[len(syllabWord) -i -1]
    return word

f = open('dataset.txt', 'w')
for i in data:
    syllabdiv = sf.fetchURL(i)
    if syllabdiv:
        f.write(i + ',' + syllabdiv + '\n')