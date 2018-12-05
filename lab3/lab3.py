import sys
from collections import Counter
import pandas as pd
from pandas import DataFrame as df
from sklearn.metrics import accuracy_score

iaa = pd.read_csv('IAA.csv')

subjectid2emptyfields = Counter()
subjectid2nontags = {}
penntreebank = set()
goldstandart = iaa.loc[0]
subjectid2wrongtag = {}
subjectid2accuracy = {}

with open('treebank.txt', 'r') as f:
    for line in f.readlines():
        line = line.strip()
        penntreebank.add(line)
f.close()

for index, row in iaa.iterrows():
    s = row
    empty = s.isin(['-']).value_counts()
    if True in empty.index:
        subjectid2emptyfields['s'+str(index)] += empty.loc[True]
    tags_used = set(s.unique())
    if '-' in tags_used:
        tags_used.remove('-')

    diff = tags_used.difference(penntreebank)
    if diff:
        subjectid2nontags['s'+str(index)] = diff

    if index != 0: #first row is gold standart
        comp = row == goldstandart
        c = list(comp).count(False)
        subjectid2wrongtag['s'+str(index)] = c
        if c == 1:
            print(comp)
        subjectid2accuracy['s'+str(index)] = accuracy_score(goldstandart, row)

print('--------------------------')
averageIaas = []
for i, row in enumerate(iaa.itertuples(index=False)):
    for i2, row2 in enumerate(iaa.itertuples(index=False)):
        if i2 > i and i > 0 and i2 > 0:
            print()
            print(i,i2)
            comp2 = pd.Series(row) == pd.Series(row2)
            comp2 = list(comp2)
            print(comp2)
            agreement = comp2.count(True)/len(comp2)
            averageIaas.append(agreement)
averageIaa = sum(averageIaas) / len(averageIaas)

print('Number of subjects: ', len(iaa))
print('Number of subjects that missed some tags: ', len(subjectid2emptyfields))
print('Usage of non existing tags: ', subjectid2nontags)
print('Subject/counts-wrong-pairs: ', subjectid2wrongtag)
print('Number of subjects with 100% correct: ', list(subjectid2wrongtag.values()).count(0))
print('Accuracy for each subject: ', subjectid2accuracy)
print('Average Accuracy: ', sum(subjectid2accuracy.values())/len(subjectid2accuracy))
print('Averaged IAA: ', averageIaa)


