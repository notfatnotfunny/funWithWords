import re
import stressFinder as sf
from collections import defaultdict, Counter
from docx import Document

counter_naiv = 0
counter_exact = 0


Adonestream=open("Adone.txt","r",encoding="utf-8")
Adonetestocompleto=Adonestream.read()

# Function to extract rhyming words from the text
def extract_rhymes(text):
    # Find words at the end of each line
    lines = text.split('\n')
    end_words = [re.findall(r'\b\w+\b', line.strip().lower())[-1] for line in lines if line.strip()]
    return end_words

# Extract rhymes from the text
rhymes = extract_rhymes(Adonetestocompleto)

def vocale(lettera):
    return lettera in 'aeiouàèéìòóù'
def consonante(lettera):
    return lettera in 'bcdfghjklmnpqrstvwxyz'

def naiveRhymeFinder(word):
    rime = word
    for i in range(len(word)-2, 0, -1):
        if vocale(word[i]) and rime == word:
            if i == len(word)-2 and (word[i] =='i' or word[i]=='u') and len(word) > 3:
                pass
            else:
                rime = word[i:]
    return rime

# Create a dictionary to count the frequencies of rhymes
rhyme_dict = defaultdict(list)
for word in rhymes:
    rime = ''
    for i in range(len(word)):
        if word[i] in 'àèéìòóù' and rime == '':
            rime = word[i:]
    if rime == '':
        rime = sf.wordToStress(word)
        if rime == 'porcodio':
            rime = naiveRhymeFinder(word)
            counter_naiv += 1
            print("naiveRhymeFinder")
        else:
            counter_exact += 1
            print("exactRhymeFinder")
            for i in range(len(rime)):
                if rime[i] in 'àèéìòóù':
                    rime = rime[i:]
                    break
    rhyme_dict[sf.rimuoviAccenti(rime)].append(word)

totalCount = counter_naiv + counter_exact
percentageNaive = 100*counter_naiv/totalCount
percentageExact = 100*counter_exact/totalCount


# Count the frequencies of words for each rhyme
rhyme_counter = {rime: Counter(words) for rime, words in rhyme_dict.items()}

# Sort the rhymes by frequency and then alphabetically
sorted_rhymes = sorted(rhyme_counter.items(), key=lambda x: (-sum(x[1].values()), x[0]))

# Create a Word document
doc = Document()
table = doc.add_table(rows=1, cols=3)
hdr_cells = table.rows[0].cells
hdr_cells[0].text = 'Rima'
hdr_cells[1].text = 'Parola-rima'
hdr_cells[2].text = 'Frequenza'

# Fill the table with sorted data
for rime, words_counter in sorted_rhymes:
    for word, count in sorted(words_counter.items(), key=lambda x: x[0]):
        row_cells = table.add_row().cells
        row_cells[0].text = rime
        row_cells[1].text = word
        row_cells[2].text = str(count)

# Save the document
output_path = 'Marino_Adone_Rhymes.docx'
doc.save(output_path)

print(f"Documento creato: {output_path}")
print("percentuale risultati esatti: ", percentageExact, '%')
print("percentuale risultati calcolati: ", percentageNaive, '%')