import spacy
from spacy.tokenizer import Tokenizer
import csv
from collections import defaultdict
import re
from pprint import pprint

nlp = spacy.load("en_core_web_sm")

def clean_text(in_file, out_file):
    nlp = spacy.load("en_core_web_sm", disable=["tok2vec", "parser", "senter", "lemmatizer", "tagger", "attribute_ruler"])
    nlp.add_pipe("merge_noun_chunks")
    nlp.add_pipe("merge_entities")
    #print('Pipeline components included: ', nlp.pipe_names)

    tokenized = {}
    reader = {}

    with open(in_file) as csv_file:
        csv_reader = csv.DictReader(csv_file, delimiter=',')
        reader = list(csv_reader)

    tokenized = reader.copy()
    for i, row in enumerate(reader):
        # remove the b's
        pattern = r'b"'
        replacement = ''
        cleaned_text = re.sub(pattern, replacement, row["text"])

        #print('Tokens: ')
        tokens = [
            token.text
            for token in nlp(cleaned_text)
            if not (
                token.is_space
            )
        ]
        
        tokens = "  ".join(tokens)
        tokenized[i]["tokens"] = tokens

        print("done with {} videos".format(i+1))

    #print(tokenized[0])
        
    print("writing data...")
    with open(out_file, 'w') as csv_file:
        fieldnames = list(tokenized[0].keys())
        writer = csv.DictWriter(csv_file, fieldnames = fieldnames, lineterminator = '\n')
        writer.writeheader()
        writer.writerows(tokenized)

clean_text("./data/june22-month-sliced.csv", "./data/june22-month-tokenized.csv")


# split with re.split(r'\s{2,}', joined)