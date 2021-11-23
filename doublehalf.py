from nltk import word_tokenize
from unicodedata import numeric
from pageScraper import urlScraper
from IngredientParser import parseTextChunk, Ingredient

def transformation(ingredient, grammar, double): 
    name, unit, amount, preperation  = parseTextChunk(ingredient, grammar)
    if len(amount) != 0:
        if len(amount) == 1:
            amount = numeric(amount)
        elif amount[-1].isdigit():
            amount = float(amount)
        else:
            amount = float(amount[:-1]) + numeric(amount[-1])
        if double: 
            amount = amount * 2 
        else: 
            amount = amount / 2
    return name, unit, amount, preperation
    

def double_half(page): 
    ingredients, _ = urlScraper(page)
    grammar = r"CHUNK: {<JJ>*<NN|NNS|NNP>}"
    totalIng = []
    for index, ingredient in enumerate(ingredients):
        name, unit, amount, preperation = transformation(ingredient, grammar, True)
        totalIng.append(Ingredient(name, unit, amount, preperation)) 
    #print ingredients 
    for item in totalIng:
        print("Name: " + item.name)
        print("Unit: " + str(item.unit))
        print("Amount: " + str(item.quantity))
        print("Preperation: " + str(item.preperation))
        print('\n')
if __name__ == '__main__':
    page = "https://www.allrecipes.com/recipe/16354/easy-meatloaf/"
    double_half(page)