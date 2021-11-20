from nltk import word_tokenize, pos_tag, RegexpParser
from unicodedata import numeric
from pageScraper import urlScraper
from IngredientParser import parseTextChunk, Ingredient
from vegetarian_pair import vegetarian_nonvegetarian, reduce_half

def replacement(sentence): 
    sentence = word_tokenize(sentence)
    for word in sentence: 
        for pair in vegetarian_nonvegetarian:
            if word in pair['non_vegetarian']:
                sentence[sentence.index(word)] = pair['vegetarian']
    ans = " ".join(sentence)
    return ans

def reducement(ingredient, grammar): 
    name, unit, amount, preperation  = parseTextChunk(ingredient, grammar)
    for pair in vegetarian_nonvegetarian:
        if name in pair['non_vegetarian']:
            name = pair['vegetarian']
    if len(amount) == 1:
        amount = numeric(amount)
    elif amount[-1].isdigit():
        amount = float(amount)
    else:
        amount = float(amount[:-1]) + numeric(amount[-1])
    if name in reduce_half: 
        amount = amount / 2 
    return name, unit, amount, preperation

def transform_vegetarian(page): 
    #page = "https://www.allrecipes.com/recipe/273320/cheesy-broccoli-stuffed-chicken-breasts/"
    ingredients, directions = urlScraper(page)
    ##grammar = r"CHUNK: {<JJ>*<NN|NNS|NNP>}"
    grammar = r"CHUNK: {<NN|NNS|NNP>}"
    totalIng = []
    for index, direction in enumerate(directions): 
        directions[index] = replacement(direction)
    for index, ingredient in enumerate(ingredients):
        ingredient = replacement(ingredient)
        print(ingredient)
        name, unit, amount, preperation = parseTextChunk(ingredient, grammar)
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

# doesnt work - says ingredient is 'skinless' and preparation is ['boneless', 'chicken', 'breast']
# transform_vegetarian('https://www.allrecipes.com/recipe/273320/cheesy-broccoli-stuffed-chicken-breasts/')

# doesnt work - 'pork meat stew' not in our list of meats
transform_vegetarian('https://www.allrecipes.com/recipe/36888/cowboy-tacos/')

#transform_vegetarian('https://www.allrecipes.com/recipe/26608/ground-beef-for-tacos/')