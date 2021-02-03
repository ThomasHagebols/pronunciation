import nltk
from nltk.corpus import wordnet
import pandas as pd
import ipywidgets as widgets
from pronouncing import rhymes, syllable_count, phones_for_word

nltk.download("wordnet")

widgets.FileUpload(
    accept=".csv",  # Accepted file extension e.g. '.txt', '.pdf', 'image/*', 'image/*,.pdf'
    multiple=False,  # True to accept multiple files upload else False
)

# Zet de naam van je excel sheet tussen de ""
df = pd.read_csv("test.csv")


def find_syn_ant(word):
    synonyms = []
    antonyms = []

    for syn in wordnet.synsets(word):
        for l in syn.lemmas():
            synonyms.append(l.name())
            if l.antonyms():
                antonyms.append(l.antonyms()[0].name())

    return set(synonyms), set(antonyms)


# nederlands,Engels woord,Engels synoniem,
df["Engels synoniem"] = df.apply(
    lambda row: find_syn_ant(row["Engels woord"])[0], axis=1
)
df["Lettergrepen"] = df.apply(
    lambda row: syllable_count(phones_for_word(row["Engels woord"])[0]), axis=1
)
df["Letters"] = df.apply(lambda row: len(row["Engels woord"]), axis=1)
df["Rijmwoord"] = df.apply(lambda row: rhymes(row["Engels woord"]), axis=1)
df["Ongerelateerd synoniem"] = df.apply(
    lambda row: find_syn_ant(row["Engels woord"])[1], axis=1
)

display(df)
