from nltk import word_tokenize, pos_tag, RegexpParser
from unicodedata import numeric
from pageScraper import urlScraper
from IngredientParser import parseTextChunk, Ingredient
from vegetarian_pair import vegetarian_nonvegetarian

def sauce_replacement(sentence): 
    sentence = word_tokenize(sentence)
    for word in range(len(sentence)): 
        if word+1 < len(sentence) and ' '.join([sentence[word], sentence[word+1]]) in vegetarian_nonvegetarian[-1]['non_vegetarian']:
            sentence[word] = vegetarian_nonvegetarian[-1]['vegetarian']
            sentence[word+1] = ''
        for pair in vegetarian_nonvegetarian:
            if word in pair['non_vegetarian']:
                sentence[word] = pair['vegetarian']
    ans = " ".join(sentence)
    return ans

def food_replacement(sentence):
    sentence = sauce_replacement(sentence)
    sentence = word_tokenize(sentence)
    for word in sentence: 
        for pair in vegetarian_nonvegetarian:
            if word in pair['non_vegetarian']:
                sentence[sentence.index(word)] = pair['vegetarian']
    ans = " ".join(sentence)
    return ans

def transform_vegetarian(page): 
    #page = "https://www.allrecipes.com/recipe/273320/cheesy-broccoli-stuffed-chicken-breasts/"
    ingredients, directions = urlScraper(page)
    ##grammar = r"CHUNK: {<JJ>*<NN|NNS|NNP>}"
    grammar = r"CHUNK: {<NN|NNS|NNP>}"
    totalIng = []
    #for index, direction in enumerate(directions): 
    #    directions[index] = sauce_replacement(direction)
    for index, direction in enumerate(directions): 
        directions[index] = food_replacement(direction)
    for index, ingredient in enumerate(ingredients):   
        ingredient = food_replacement(ingredient)
        print(ingredient)
        name, unit, amount, preperation = parseTextChunk(ingredient, grammar)
        for substitute_pair in vegetarian_nonvegetarian:
            if substitute_pair['vegetarian'] in name and len(name) > len(substitute_pair['vegetarian']):
                name = substitute_pair['vegetarian']
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
#transform_vegetarian('https://www.allrecipes.com/recipe/36888/cowboy-tacos/')

#transform_vegetarian('https://www.allrecipes.com/recipe/26608/ground-beef-for-tacos/')

#transform_vegetarian('https://www.allrecipes.com/recipe/265400/easy-baked-fish-with-lemon/')

#transform_vegetarian('https://www.allrecipes.com/recipe/257954/caribbean-fish-soup/')

#transform_vegetarian('https://www.allrecipes.com/recipe/247235/lechon-manok-pinoy-roast-chicken/')