from nltk import word_tokenize
from unicodedata import numeric
from pageScraper import urlScraper
from IngredientParser import parseTextChunk, Ingredient
from healthy_pair import healthy_unhealthy, reduce_half

def replacement(sentence): 
    sentence = word_tokenize(sentence)
    for word in sentence: 
        for pair in healthy_unhealthy:
            if word in pair['unhealthy']:
                word = pair['healthy']
    ans = " ".join(sentence)
    return ans

def reducement(ingredient, grammar): 
    name, unit, amount, preperation  = parseTextChunk(ingredient, grammar)
    for pair in healthy_unhealthy:
        if name in pair['unhealthy']:
            name = pair['healthy']
    if len(amount) != 0:
        if len(amount) == 1:
            amount = numeric(amount)
        elif amount[-1].isdigit():
            amount = float(amount)
        else:
            amount = float(amount[:-1]) + numeric(amount[-1])
        if name in reduce_half: 
            amount = amount / 2 
    return name, unit, amount, preperation
    

def transform_healthy(page): 
    #page = "https://www.allrecipes.com/recipe/16354/easy-meatloaf/"
    ingredients, directions = urlScraper(page)
    grammar = r"CHUNK: {<JJ>*<NN|NNS|NNP>}"
    totalIng = []
    for index, direction in enumerate(directions): 
        directions[index] = replacement(direction)
    for index, ingredient in enumerate(ingredients):
        ingredient = replacement(ingredient)
        name, unit, amount, preperation = reducement(ingredient, grammar)
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
if __name__ == '__main__':
    page = "https://www.allrecipes.com/recipe/16354/easy-meatloaf/"
    transform_healthy(page)