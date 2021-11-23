from nltk.sem.evaluate import is_rel
from StyleUrl import gatherIngredients, gatherURLs, main
from nltk import word_tokenize, pos_tag, RegexpParser
from unicodedata import numeric
from pageScraper import urlScraper
from IngredientParser import Recipe, parseTextChunk, Ingredient
from copy import deepcopy
import copy
import random
import re





def toIndian(url):
    ingredients, instructions = urlScraper(url)
    styleKey = gatherIngredients()
    oldRec = Recipe(url)
    newIng = []
    oldIng = copy.deepcopy(oldRec.ingredients)
    dels = {}
    for i, item in enumerate(oldIng):
        sty = item.type
        if sty == "?" or sty == "G":
            continue
        potSwap = styleKey[sty]
        choice = random.choice(potSwap)
        while choice == "":
            choice = random.choice(potSwap)
        dels[oldRec.ingredients[i].name] = choice
        oldRec.ingredients[i].name = choice
        newIng.append(oldRec.ingredients[i].name)
        
        #for swap in potSwap:
        #    if len(potSwap) <= 1:
        #        oldRec.ingredients[i].name = swap
        #        newIng.append(oldRec.ingredients[i])
        #        break
        #    if any(set(swap.strip().split(' ')).intersection(set(example.name.lower().split(' '))) for example in oldIng):
        #        continue
        #    oldRec.ingredients[i].name = swap
        #    newIng.append(oldRec.ingredients[i])
        #    break
    for key in dels:
        if re.search("butter", key):
            dels[key] = "ghee clarified butter"
    return dels, newIng
    print("Done")



def transform_indian(page): 
    #page = "https://www.allrecipes.com/recipe/273320/cheesy-broccoli-stuffed-chicken-breasts/"
    dels, news = toIndian(page)
    ingredients, directions = urlScraper(page)
    lisDels = dels.keys()
    ##grammar = r"CHUNK: {<JJ>*<NN|NNS|NNP>}"
    grammar = r"CHUNK: {<NN|NNS|NNP>}"
    totalIng = []
    for index, direction in enumerate(directions):
        directions[index] = replacement(direction, dels, news)
    for index, ingredient in enumerate(ingredients):
        ingredient = replacement(ingredient, dels, news)
        print(ingredient)
        name, unit, amount, preperation = parseTextChunk(ingredient, grammar)
        for d in dels:
            if dels[d] in name and len(name) > len(dels[d]):
                name = dels[d]
        totalIng.append(Ingredient(name, unit, amount, preperation)) 
    #print ingredients 
    for item in totalIng:
        print("Name: " + item.name)
        print("Unit: " + str(item.unit))
        print("Amount: " + str(item.quantity))
        print("Preperation: " + str(item.preperation))
        print('\n')
    #print directions
    for index, direction in enumerate(directions): 
        print("Step {}: {} \n".format(index + 1, direction))

def replacement(sentence, dels, news): 
    token = word_tokenize(sentence)
    for word in token:
        for d in dels:
            tempWord = word.replace(".", "")
            tempWord = word.replace(",", "")
            tempWord = word.lower()
            tempD = d.replace(".", "")
            tempD = d.replace(",", "")
            tempD = d.lower()
            if tempWord in tempD and word != " " and len(word) > 2 and word in token:
                token[token.index(word)] = dels[d]
    indDel = []
    for i,word in enumerate(token):
        if i<(len(token)-1) and word == token[i+1]:
            indDel.append(i+1)
    indDel = list(reversed(indDel))
    for item in indDel:
        del(token[item])

    sentence = " ".join(token)
    return sentence

def sim(ing, sen):
    cnt = 0
    ind = []
    ing = ing.split(" ")
    newSen = sen.split(" ")
    sen = sen.split()
    for i, item in enumerate(newSen):
        newSen[i] = newSen[i].replace(".", "")
        newSen[i] = newSen[i].replace(",", "")
    for i in ing:
        if i in newSen:
            if len(ind) == 0:
                ind.append(newSen.index(i))
            elif ind[-1] + 1 != newSen.index(i):
                ind.append(newSen.index(i))
                

            
    return cnt, ind


def IndianTransform(url):
    transform_indian(url)

def main():
    transform_indian("https://www.allrecipes.com/recipe/45361/easy-bake-fish/")

if __name__ == '__main__':
    main()