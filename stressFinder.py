import requests
from bs4 import BeautifulSoup
import re
import formeFlesse as ff

###### pip install requests beautifulsoup4 ######

# PRE: stringa
# POST: sostituzione di vocali accentate con vocali non accentate e stringa resa minuscola

def rimuoviAccenti(stringa):
    ritorno = stringa.lower()
    ritorno = re.sub(r'[àáâãäå]', 'a', ritorno)
    ritorno = re.sub(r'[èéêë]', 'e', ritorno)
    ritorno = re.sub(r'[ìíîï]', 'i', ritorno)
    ritorno = re.sub(r'[òóôõö]', 'o', ritorno)
    ritorno = re.sub(r'[ùúûü]', 'u', ritorno)
    return ritorno 


def accent(lettera):
    res = lettera

    if lettera == 'a':
        res = 'à'
    elif lettera == 'e':
        res = 'è'
    elif lettera == 'i':
        res = 'ì'
    elif lettera == 'o':
        res = 'ò'
    elif lettera == 'u':
        res = 'ù'
    
    return res


# def treccani(parola):

#     url = f"https://www.treccani.it/vocabolario/{rimuoviAccenti(parola)}/"
#     url_1 = f"https://www.treccani.it/vocabolario/{rimuoviAccenti(parola)}1/"
#     url_2 = f"https://www.treccani.it/vocabolario/{rimuoviAccenti(parola)}2/"

#     response = requests.get(url)
#     html_content = response.content

#     pronunce = []

#     urlList = [url, url_1, url_2]

#     for url in urlList:
#         response = requests.get(url)
#         html_content = response.content

#         soup = BeautifulSoup(html_content, 'html.parser')
#         script_tag = soup.find('div', id='__next')
#         culo = script_tag.find_all('strong', 'MuiTypography-root MuiTypography-body1 css-1rmcmsc')
#         searchType = script_tag.find('p', 'MuiTypography-root MuiTypography-leadP HeroBase_leadP__0yoSv css-2hffjm')

#         if searchType:
#             searchType = str(searchType)[1:-1].split('>')[-1].split('<')[0]
#             if searchType == 'Vocabolario on line':
#                 for i in culo:
#                     i = str(i)[1:-1]
#                     i = i.split('>')[-1].split('<')[0]
#                     if i.split(' ')[0][-1]!='.' and i not in pronunce:
#                         pronunce.append(i)

#     return pronunce


def wordToStress(parola):
    culo = fetchURL(parola)

    if culo:
        return culo
    else:
        parola_1 = parola + '_2'
        culo = fetchURL(parola_1)
    
    if culo:
        return culo
    
    nonPoeticWord = ff.formaNonFlessa(parola[:-1]+'v'+parola[-1])
    if nonPoeticWord:
        if 'impf' in nonPoeticWord[0][2].split('+'):
            return parola[:-2]+accent(parola[-2])+parola[-1]
    
    parole = ff.formaNonFlessa(parola)

    # non si sa o non è una forma flessa [*superfluo*]
    for j in parole:
        if len(j)==1 or j[1]==parola:
            culo = fetchURL(parola)
            if culo:
                return culo
            else:
                parola_1 = parola + '_2'
                culo = fetchURL(parola_1)
    
    # è una forma flessa!
    # priorità ai sostantivi
    for j in parole:
        if not culo:
            if j[2][:4]=='NOUN' or j[2][:3]=='ADJ' or j[2][:3]=='DET':
                culo = fetchURL(j[1])
                if culo:
                    for i in range(len(culo)):
                        if j[0][-5:] in ['trice', 'trici']:
                            culo = j[0][:-3] + accent(j[0][-3]) + j[0][-2:]
                            break
                        if culo[i] in 'àèéìòóù':
                            if len(j[0])>i+2 and j[0][i+1:i+3] in ['ei','oi']: # miei -x-> mìei, tuoi -x-> tùoi
                                culo = rimuoviAccenti(culo[:i+1]) + accent(j[0][i+1]) + j[0][i+2:]
                            else:
                                culo = culo[:i+1]+j[0][i+1:] #dei -x-> dìei non succede perché esiste come prep. art. su dizionari.corriere.it
                            break
                    return culo
                else:
                    new_try = j[1] + '_2'
                    culo = fetchURL(new_try)
                    if culo:
                        for i in range(len(culo)):
                            if culo[i] in 'àèéìòóù':
                                culo = culo[:i+1]+j[0][i+1:]
                                break
                        return culo
        else:
            break
    
    # for j in parole:
    #     if not culo:
    #         if j[2][:3]=='ADJ':
    #             culo = fetchURL(j[1])
    #             if culo:
    #                 for i in range(len(culo)):
    #                     if culo[i] in 'àèéìòóù':
    #                         culo = culo[:i+1]+j[0][i+1:]
    #                         break
    #                 return culo
    #             else:
    #                 new_try = j[1] + '_2'
    #                 culo = fetchURL(new_try)
    #                 if culo:
    #                     for i in range(len(culo)):
    #                         if culo[i] in 'àèéìòóù':
    #                             culo = culo[:i+1]+j[0][i+1:]
    #                             break
    #                     return culo
    #     else:
    #         break
    
# non si sa o è un verbo

    # for j in parole:
    #     if not culo:
    #         if j[2][:3] == 'VER':
    #             culo = fetchURL(j[1])
    #             if culo:
    #                 radice = ''
    #                 if rimuoviAccenti(culo[-4:]) in ['iare', 'iere']:
    #                     radice = rimuoviAccenti(culo[:-4])
    #                 else:
    #                     radice = rimuoviAccenti(culo[:-3])

    #                 if j[2][4:12] == 'ind+pres' and j[2][-3:] in ['1+s', '2+s', '3+s', '3+p']:
    #                     for i in range(len(radice)-1, -1, -1):
    #                         if radice[i] in 'aeiouàèéìòóù':
    #                             radice = radice[0:i] + accent(radice[i]) + radice[1+i-len(radice):]
    #                             break
    #                     culo = radice + parola[len(radice):]
    #                 else:
    #                     culo = ''
    #                 ##### mancano tutti gli altri tempi verbali #####
    #     else:
    #         break
    
    if not culo:
        culo = 'porcodio'
        

    return culo

def fetchURL(parola, syllabDivision=False):

    url = f"https://dizionari.corriere.it/dizionario_italiano/{parola[0].upper()}/{rimuoviAccenti(parola)}.shtml"
    
    response = requests.get(url)
    html_content = response.content

    soup = BeautifulSoup(html_content, 'html.parser')
    script_tag = soup.find('main', id='l-main')
    culo = script_tag.find('span', 'pron')

    if culo:
        culo = str(culo)[20:-7]
        culo = culo.replace(']','')
        if ' ' in culo:
            culo = culo.split()[0].replace(',','')
        if(not syllabDivision):
            culo = culo.replace('-','')
        else:
            culo = culo.split('-')
    
    return culo

parola = 'stupore'
print(wordToStress(parola))
# print(treccani(parola))

