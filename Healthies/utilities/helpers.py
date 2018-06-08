import json
import pandas as pd
import sys
import os
import csv
from pprint import pprint
from tqdm import tqdm


sys.path.append('..')

def load_data():
    with open("../data/user_data.json", "r") as infile:
        userData = json.load(infile)
    with open("../data/madeRecipeUsers.json", "r") as infile:
        recipesUsers = json.load(infile)
        
    return userData, recipesUsers

def load_recipe(recipe_id):
    with open("../data/recipe_data/" + str(recipe_id) + "/data.json", "r") as infile:
        recipeData = json.load(infile)
    return recipeData

def load_all_recipes():
    directory = '../data/recipe_data/'

    columns_recipes=['id','total_time','ingredients', 'instructions', 'health_score']
    columns_nutrition=['id','sodiumContent','carbohydrateContent','fatContent','proteinContent','calories','cholesterolContent']
    recipes = pd.DataFrame(columns=columns_recipes)
    nutrition = pd.DataFrame(columns=columns_nutrition)
    
    #writer_recipes = pd.ExcelWriter(open('recipes.xlsx', "w"), fieldnames=columns_recipes)
    #writer_recipes.writeheader()

    br=0
    items = []
    for path, subdirs, files in tqdm(os.walk(directory)):
        row_recipe={}
        for name in files:
            filename = os.path.join(path, name)
            if name == 'data.json':
                with open(filename) as json_data:
                    recipe_info = json.load(json_data)
                    row_recipe.update({'id': path[path.rfind('/')+1:], 
                                    'total_time': recipe_info['ready_time'],
                                    'ingredients':recipe_info['ingredients'],
                                    'instructions':recipe_info['instructions']
                               })
            if name == 'healthscore.json':
                with open(filename) as json_data:
                    recipe_info = json.load(json_data)
                    row_recipe.update({'health_score':recipe_info['score']})
                #recipes.append(row_recipe[0], ignore_index=True)
                #writer_recipes.write(row_recipe[0])
                #with open('../data/recipes.json', 'a') as outfile:  
                #    json.dump(row_recipe, outfile)
            if name == 'nutrition.json':
                with open(filename) as json_data:
                    recipe_info = json.load(json_data)
                    nutrients = sorted(recipe_info['nutrition'].keys())
                    for nutrient in nutrients:
                        row_recipe.update({nutrient:recipe_info['nutrition'][nutrient]})
                items.append(row_recipe)
          
    with open('../data/recipes.json', 'w') as outfile:      
        json.dump(items, outfile)
    #recipes.to_pickle('../data/recipes.pkl')
        
    
def clear_ingredient(ingredient):
    m = re.match('[-]?[0-9]+[,. ]?[0-9]*([\/][0-9]+[,.]?[0-9]*)*', ingredient)
    if m is not None:
        o = re.match('\([-]?[0-9]+[,. ]?[0-9]*([\/][0-9]+[,.]?[0-9]*)* ?[a-z]*[A-Z]*\)', ingredient[m.end():])
        if o is not None:
            b = re.match('[-]?[0-9]+[,. ]?[0-9]*([\/][0-9]+[,.]?[0-9]*)*', o.group()[1:-1])
            if stemmer.stem(o.group()[1:-1].split()[-1]) in units:
                return stemmer.stem(ingredient[o.end()+len(o.group()[1:-1].split()[-1]):])
        
            else:
                return stemmer.stem(ingredient[len(o.group())+m.end()+len(o.group()[1:-1].split()[-1])+1:])
        else:
            ing_parts =  nltk.word_tokenize(ingredient)
            ing_parts_stemmed = [stemmer.stem(word) for word in ing_parts]
            for i, part in enumerate(ing_parts_stemmed):
                if part in units:
                    return ingredient[m.end()+len(ing_parts[i])+1:]
            return ingredient[m.end():] 
    else:
        return ingredient

        