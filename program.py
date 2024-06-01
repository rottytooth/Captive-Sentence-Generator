import math
from nltk import CFG
from nltk.parse.generate import generate, demo_grammar
import numpy as np
import random
import warnings
warnings.filterwarnings('ignore', category=UserWarning)
import pandas as pd


# max number of special characters per word
WORD_LIMIT = 5

# noun, verb, adjective, adverb, or adjective satellite
parts_of_speech = ['n', 'v', 'a', 'r', 's']

# attributive, predicative, or immediately postpositive
adj_types = ['a', 'p', 'ip']

no_captive = '[^bdfghjklpqty]*'

# WORDNET 3.1
voc = pd.read_json('vocab/wordnet31.json')

# ADDITIONAL VOCAB (prepositions, conjunctions, etc.)
ca_voc = pd.read_json('vocab/additional.json')

# build grammar
with open('english.cfg', 'r') as f:
    grammar = f.read()
grammar += "\nN -> 'test'"
# voc[voc['pos'].str.contains("n")] # all nouns
cfg = CFG.fromstring(grammar)


def generate_word(pattern, type=None):
    if type is None:
        type = random.choice(parts_of_speech)

    resp = '^' + no_captive
    for p in pattern:
        resp += p + no_captive
    resp += '$'

    if type == 'a':
        type = 'a|s'

    filt = voc[voc['lemma'].str.contains(resp)]
    filt = filt[voc['pos'].str.contains(type)]
    filt = filt.sample(frac=1) # randomize

    if filt.empty:
        raise Exception(f'Could not match pattern "{pattern}" with pos {type}.')

    return filt.iloc[0]['lemma']

def split_program(program):
    total = len(program)
    wordsize = math.ceil(total/2) + 1
    dist = np.random.randint(1, WORD_LIMIT, size=wordsize)
    while sum(dist) != total and not len([*filter(lambda x: x >= WORD_LIMIT, dist)]) > 0:
        dist = np.random.randint(0, WORD_LIMIT, size=wordsize)    
    # print(dist) 
    wordset = []
    last = 0
    for i in dist:
        # print(f"last: {last}, i: {i}")
        wordset.append(program[last:last+i])
        last += i
    return wordset

# print(generate_word('t', 'r'))

program = 'ldgptyldpytthtt'
words = split_program(program)

outstr = ''
for w in words:
    outstr += ' ' + generate_word(w)

print(outstr)

