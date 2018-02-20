import gensim
import warnings
from nltk.tokenize import word_tokenize


# run with command: python -w ignore similarityChecker.py

def find_similarity(pathOfFile1, pathOfFile2):
    file1Data = open(pathOfFile1).read()
    file2Data = open(pathOfFile2).read()
    documents = []
    documents.append(file1Data)
    documents.append(file2Data)
    gen_docs = [[w.lower() for w in word_tokenize(text)] for text in documents]
    dictionary = gensim.corpora.Dictionary(gen_docs)

    corpus = [dictionary.doc2bow(gen_doc) for gen_doc in gen_docs]

    dictionary1 = {}
    dictionary2 = {}

    for data in (corpus[0]):
        dictionary1[data[0]] = data[1]

    for data in (corpus[1]):
        dictionary2[data[0]] = data[1]

    similarity = 0.0

    for i in range(len(dictionary)):
        if (i in dictionary1 and i in dictionary2):
            similarity = similarity + min(dictionary1[i], dictionary2[i])

    return (similarity / min(len(corpus[0]), len(corpus[1])))


print(findSimilarity('text1.txt', 'text2.txt'))
