import json
import numpy as np
from collections import Counter

def sample_neg(u,tr,tot_items):
  sample = tr[0]
  while sample in tr:
    neg_idx = np.random.randint(0,len(tot_items))
    sample  = tot_items[neg_idx]
  return sample

with open("data/userRecipes.json", "r") as file:
  userRecipes = json.loads(file.read())

with open("data/recipeUsers.json", "r") as file:
  recipeUsers = json.loads(file.read())

te = {}
tr = {}

tr_items  = []
tot_items = set()

for k,v in userRecipes.items():
  if len(v)<5:
    continue

  for i in v:
    tot_items.add(i)

  test_idx = np.random.randint(0,len(v))
  te[k]  = v[test_idx]
  del v[test_idx]
  tr[k] = v
  tr_items += v

tot_items       = list(set(tot_items))
tr_items_unique = list(set(tr_items))

pop = Counter(tr_items)

auc       = 0.0
test_step = 0
for k,v in te.items():

  neg = sample_neg(k,tr[k],tr_items_unique)

  sp = pop[v]
  sn = pop[neg]

  if sp>sn:
    auc += 1.0
  elif sp==sn:
    auc += 0.5

  test_step += 1

print("AUC: ", auc / test_step)


interactions_te = {}
for user in userRecipes.keys():
  idx = np.random.randint(0,len(userRecipes[user]))
  interactions_te[user]  = (userRecipes[user][idx], user)

recipes = list(recipeUsers.keys())

def sample_neg_nathan(recipes, user, userRecipes):
  recipe  = recipes[np.random.randint(0, len(recipes))]
  while recipe in userRecipes[user]:
      recipe = np.random.choice(recipes)
  return recipe

print("Computing AUC of dummy ranker...")
# Compute the Area Under the Curve (AUC)
auc = 0;
for interaction in interactions_te:
  recipe = interaction[0]
  user = interaction[1]
  n_recipe = sample_neg_nathan(recipes, user, userRecipes)

  sp = len(recipeUsers[recipe])
  sn = len(recipeUsers[n_recipe])

  if sp > sn:
    auc = auc+1
  else:
    if sp == sn:
      auc = auc+0.5

auc = auc / len(userRecipes_te.keys())
print("AUC test: " + str(auc))

