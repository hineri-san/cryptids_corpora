import os
import sys
import re

from natasha import (
    Segmenter,
    MorphVocab,
    NamesExtractor,
    NewsMorphTagger,
    NewsNERTagger,
    NewsEmbedding,
    Doc
)

from dawg_python import RecordDAWG
from pymorphy2 import MorphAnalyzer, units

emb = NewsEmbedding()
segmenter = Segmenter()
morph_vocab = MorphVocab()
ner_tagger = NewsNERTagger(emb)
morph_tagger = NewsMorphTagger(emb)


def download_texts():
    wordss_dict = {}
    mypath = 'text'
    onlyfiles = [f for f in os.listdir(mypath) if os.path.isfile(os.path.join(mypath, f))]
    for i in onlyfiles:
        author, name = i.split(' - ')
        wordss_dict = extract_fact(author, name, i, wordss_dict)
    return wordss_dict


def all_forms(word, pos):
    path = '/usr/local/lib/python3.6/dist-packages/pymorphy2_dicts_ru/data'

    m = MorphAnalyzer(path=path, units=[units.DictionaryAnalyzer()])

    d = RecordDAWG(str('>HH'))
    d.load(path + '/words.dawg')

    seen = []
    for list_words in m.parse(word):
        for p in list_words.lexeme:
            if p.tag.POS == pos:
                seen.append(p.word)

    return(seen)


def extract_fact(author, name, path, wordss_dict = {}):

    wordss = ""

    with open('text/' + path, 'r') as txtfile:
        wordss = txtfile.read()

    for words in re.split('\.\n|\.\ ', wordss):
        if not words:
            continue

        doc = Doc(words.replace('\n', ' '))
        doc.segment(segmenter)
        doc.tag_morph(morph_tagger)
        doc.tag_ner(ner_tagger)

        for token in doc.tokens:
            token.lemmatize(morph_vocab)
            wordss_dict.setdefault(author, {name: {}})
            wordss_dict[author].setdefault(name, {})
            wordss_dict[author][name].setdefault(words, [])
            wordss_dict[author][name][words].append({
                "word": token.text.lower(),
                "pos": token.pos,
                "lemma": token.lemma
            })

    return wordss_dict


def lemmatize_word(word):
    doc = Doc(word)
    doc.segment(segmenter)
    doc.tag_morph(morph_tagger)
    doc.tag_ner(ner_tagger)

    for token in doc.tokens:
        token.lemmatize(morph_vocab)
        return token.lemma

    return word

def search(wordss_dict, find_text_raw):
    find_text = find_text_raw.split(' ')
    match = []
    find_list = []
    # sequence = [0 for _ in range(len(find_text))]
    sequence = []

    if len(find_text) > 3:
        return match

    for i in find_text:
        if len(re.findall(r'[А-я]+', i)) == 0:
            find_list.append({'find_str': 'pos', 'text': i})
        elif i.find('+') > -1:
            word, pos = i.split('+')
            text = all_forms(word, pos)

            find_list.append({'find_str': 'word', 'text': text})
        elif i.find('"') > -1:
            find_list.append({'find_str': 'word', 'text': i.replace('"', '')})
        else:
            find_list.append({'find_str': 'lemma', 'text': lemmatize_word(i)})

    find_list_temp = find_list.copy()

    for author, names in wordss_dict.items():
        for name, list_text in names.items():
            for text, pr in list_text.items():
                find_list_temp = find_list.copy()

                for p in pr:

                    for idx, f_text in enumerate(find_list_temp):

                        if isinstance(f_text['text'], list):
                            for i in f_text['text']:
                                if p[f_text['find_str']] == i:
                                    sequence.append(1)
                                    find_list_temp.pop(idx)
                                    break

                        elif p[f_text['find_str']] == f_text['text']:
                            sequence.append(1)
                            find_list_temp.pop(idx)
                            break

                        elif len(sequence) > 0 and len(find_text) > len(sequence):
                            find_list_temp = find_list.copy()
                            sequence = []
                            break

                    if len(sequence) > 0 and len(sequence) == len(find_text) and all(sequence):
                        if [author, name, text] not in match:
                            match.append([author, name, text])
                        find_list_temp = find_list.copy()
                        sequence = []

    return match

# texts = download_texts()
# result = search(texts, 'объект')
# pass
