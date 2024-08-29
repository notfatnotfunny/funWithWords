import re 


with open("morph-it_048.txt", encoding='latin-1') as morphIt_048:
    morphIt = morphIt_048.read()

parole = morphIt.split('\n')

culo = [[word for word in line.split("\t")]for line in parole]


def formaNonFlessa(parola):

    risultato = []

    for riga in culo:
        if riga[0] == parola:
            risultato.append(riga)
            risultato.append(riga)
    
    # if not risultato:
    #     risultato.append([parola])
    
    new_list = []
    for i in risultato:
        if i not in new_list:
            new_list.append(i)
    
    return new_list 

#print(formaNonFlessa("desia"))