from nltk import word_tokenize
from pageScraper import urlScraper
from IngredientParser import parseTextChunk, Ingredient
from lactosefree_pair import lactosefree_lactose

def trigram_replacement(sentence): 
    sentence = word_tokenize(sentence)
    for word in range(len(sentence)):
        for pair in lactosefree_lactose:
            if word+2 < len(sentence) and ' '.join([sentence[word], sentence[word+1], sentence[word+2]]) in pair['lactose']:
                sentence[word] = pair['lactose-free']
                sentence.pop(word+1)
                sentence.pop(word+2)
    ans = " ".join(sentence)
    return ans

def bigram_replacement(sentence): 
    sentence = word_tokenize(sentence)
    for word in range(len(sentence)):
        for pair in lactosefree_lactose:
            if word+1 < len(sentence) and ' '.join([sentence[word], sentence[word+1]]) in pair['lactose']:
                sentence[word] = pair['lactose-free']
                sentence.pop(word+1)
    ans = " ".join(sentence)
    return ans

def lactose_replacement(sentence):
    sentence = trigram_replacement(sentence)
    sentence = bigram_replacement(sentence)
    sentence = word_tokenize(sentence)
    for word in sentence: 
        for pair in lactosefree_lactose:
            if word in pair['lactose']:
                sentence[sentence.index(word)] = pair['lactose-free']
    ans = " ".join(sentence)
    return ans

def transform_lactosefree(page): 
    ingredients, directions = urlScraper(page)
    grammar = r"CHUNK: {<NN|NNS|NNP>}"
    totalIng = []
    for index, direction in enumerate(directions): 
        directions[index] = lactose_replacement(direction)
    for index, ingredient in enumerate(ingredients):   
        ingredient = lactose_replacement(ingredient)
        print(ingredient)
        name, unit, amount, preperation = parseTextChunk(ingredient, grammar)
        for substitute_pair in lactosefree_lactose:
            if substitute_pair['lactose-free'] in name and len(name) > len(substitute_pair['lactose-free']):
                name = substitute_pair['lactose-free']
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
