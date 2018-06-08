#wass distance

from itertools import product
from collections import defaultdict
from tqdm import tqdm

import numpy as np
import pandas as pd

from scipy.spatial.distance import euclidean
import pulp


singleindexing = lambda m, i, j: m*i+j
unpackindexing = lambda m, k: (k/m, k % m)


def tokens_to_fracdict(tokens):
    cntdict = defaultdict(lambda : 0)
    for token in tokens:
        cntdict[token] += 1
    totalcnt = sum(cntdict.values())
    return {token: float(cnt)/totalcnt for token, cnt in cntdict.items()}


# use PuLP
def word_mover_distance_probspec(recipe_1, recipe_2, wvmodel, histograms, lpFile=None):
    #d1 = quantity_map_normalized_pruned.loc[recipe1].iloc[quantity_map_normalized_pruned.loc[recipe1].nonzero()]
    #d2 = quantity_map_normalized_pruned.loc[recipe2].iloc[quantity_map_normalized_pruned.loc[recipe2].nonzero()]
    
    all_tokens = list(set(list(histograms[recipe_1].keys())+list(histograms[recipe_2].keys())))
    wordvecs = {token: wvmodel[token] for token in all_tokens}
    
    first_sent_buckets = histograms[recipe_1]#tokens_to_fracdict(first_sent_tokens)
    second_sent_buckets = histograms[recipe_2]#tokens_to_fracdict(second_sent_tokens)

    T = pulp.LpVariable.dicts('T_matrix', list(product(all_tokens, all_tokens)), lowBound=0)
    prob = pulp.LpProblem('WMD', sense=pulp.LpMinimize)
    prob += pulp.lpSum([T[token1, token2]*euclidean(wordvecs[token1], wordvecs[token2])
                        for token1, token2 in product(all_tokens,all_tokens)])
    for token2 in second_sent_buckets:
        prob += pulp.lpSum([T[token1, token2] for token1 in first_sent_buckets])==second_sent_buckets[token2]
    for token1 in first_sent_buckets:
        prob += pulp.lpSum([T[token1, token2] for token2 in second_sent_buckets])==first_sent_buckets[token1]

    if lpFile!=None:
        prob.writeLP(lpFile)

    prob.solve()
    return prob


def word_mover_distance(first_sent_tokens, second_sent_tokens, wvmodel, histograms, lpFile=None):
    prob = word_mover_distance_probspec(first_sent_tokens, second_sent_tokens, wvmodel,histograms,  lpFile=lpFile)
    return pulp.value(prob.objective)
 
    
recipes = pd.read_json('../data/recipes_clean.json')
ingredients = set([ingredient['id'] for ingredients in recipes['ingredients'] for ingredient in ingredients])

with open ('data_exp.txt', 'w') as fo:
    for i, ingredients in tqdm(enumerate(recipes['ingredients'])):
        ids = [ingredient['id'] for ingredient in ingredients]
        fo.write(' '.join(i for i in ids))
        fo.write('\n')
        
import fasttext
model = fasttext.cbow('data_exp.txt', 'model', dim=40, min_count = 5, epoch=20)
classifier = fasttext.supervised('data_exp.txt', 'model', label_prefix='__label__nesto')

        
quantity_map_normalized_pruned = pd.read_csv('qmnp.csv', ',',  index_col='id')
histograms = quantity_map_normalized_pruned.apply(lambda x: x.iloc[x.nonzero()].to_dict(), axis=1)#x.iloc[x.nonzero()], axis=1)
recipe_id = 100008
dict_wass={}

import datetime
print(datetime.datetime.now())
print('finding similar recipes for recipe 100008')
for recipe in tqdm(list(quantity_map_normalized_pruned.index)):
    dict_wass.update({recipe:word_mover_distance(recipe_id, recipe, model, histograms)})
np.save('wass_distances', dict_wass)
