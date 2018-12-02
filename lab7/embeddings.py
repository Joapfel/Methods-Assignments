import string
import math
import spacy
from collections import Counter

def getContext(L, i):
    left = []
    right = []
    if i >= 3:
        left = L[i-3:i]
    else:
        left = L[0:i]
    if i < len(L)-1:
        right = L[i+1:i+4]
    #return left,right
    return left + right

def cosineSimilarity(vec1, vec2):
    dot = 0
    len1, len2 = 0,0
    for v1,v2 in zip(vec1, vec2):
        dot += (float(v1) * float(v2))
        len1 += (float(v1) * float(v1))
        len2 += (float(v2) * float(v2))
    len1 = math.sqrt(float(len1))
    len2 = math.sqrt(float(len2))
    return dot / (float(len1) * float(len2))

nlp = spacy.load('en')
doc = nlp(open('minicorpus.txt').read())


bag = set()
for t in doc:
    tag = t.tag_
    lemma = t.lemma_
    if tag in ['NN', 'NNS', 'NNP'] or tag in ['VBZ', 'VBG', 'VBP'] or tag in ['JJ',
                                                                       'JJR',
                                                                       'JJS']:
        print(t, t.lemma_, t.tag_)
        bag.add(str(lemma))

c = Counter({x:0 for x in bag})

batman = c.copy()
joker = c.copy()
wayne = c.copy()
sentences = [t for t in doc.sents]
for sentence in sentences:
    sentence = str(sentence).translate(str.maketrans('', '', string.punctuation))
    sentence = ' '.join(sentence.split())
    sentlist = [t.lemma_ for t in nlp(sentence)]
    for i,t in enumerate(sentlist):
        if t == 'batman':
            context = getContext(sentlist, i)
            print(context)
            for con in context:
                if con in batman.keys():
                    batman[con] += 1

        elif t == 'joker':
            context = getContext(sentlist, i)
            for con in context:
                if con in joker.keys():
                    joker[con] += 1

        elif t == 'wayne':
            context = getContext(sentlist, i)
            for con in context:
                if con in wayne.keys():
                    wayne[con] += 1

print(batman)
print(joker)
print(wayne)

vocab = [t for t in bag]
print(vocab)

batman_vec = [batman[t] for t in vocab]
joker_vec = [joker[t] for t in vocab]
wayne_vec = [wayne[t] for t in wayne]

print("batman vec: ", batman_vec)
print("joker vec: ", joker_vec)
print("wayne vec: ", wayne_vec)
print()

#print("batman batman: ", cosineSimilarity(batman_vec, batman_vec))

print("batman wayne similarity: ", cosineSimilarity(batman_vec, wayne_vec))
print("joker wayne similarity: ", cosineSimilarity(joker_vec, wayne_vec))
print("batman joker similarity: ", cosineSimilarity(batman_vec, joker_vec))


google_vecs = {t.split()[0]:t.split()[1:] for t in open('GoogleNews-subset').readlines()}
print("batman wayne google embedings similiarity: ",
      cosineSimilarity(google_vecs['Batman'], google_vecs['Wayne']))
print("joker wayne google embedings similiarity: ",
      cosineSimilarity(google_vecs['Joker'], google_vecs['Wayne']))
print("batman joker google embedings similiarity: ",
      cosineSimilarity(google_vecs['Batman'], google_vecs['Joker']))
