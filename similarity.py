from __future__ import division
import re
import gensim.similarities.docsim as sim

def words(text):
    return re.findall('\w+', text)

def bigrams(list):
    bi = set()
    for i in xrange(len(list) - 1):
        bi.add(list[i] + ' ' + list[i + 1])

    return bi

def jaccards_similarity(text1, text2):
    words1 = words(text1)
    words2 = words(text2)
    bi1 = bigrams(words1)
    bi2 = bigrams(words2)

    toret = len(bi1.intersection(bi2))
    toret = toret / len(bi2.union(bi1))
    return toret



if __name__ == '__main__':
    text = 'this is some tie that I want to test out'
    text2 = 'this is some other text to test'
    print jaccards_similarity(text, text2)

    simi = sim.Similarity()