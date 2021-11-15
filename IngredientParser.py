from nltk import word_tokenize, pos_tag
from pageScraper import urlScraper
import re
measure_regex = '(cup|spoon|fluid|ounce|pinch|gill|pint|quart|gallon|pound|drops|recipe|slices|pods|package|can|head|halves)'
tool_indicator_regex = '(pan|skillet|pot|sheet|grate|whisk|griddle|bowl|oven|dish)'
method_indicator_regex = '(boil|bake|baking|simmer|stir|roast|fry)'
time_indicator_regex = '(min|hour)'

class Ingredient:
    def __init__(self, name, unit, quantity=None):
        self.name = name
        self.quantity = quantity
        self.unit = unit
    
def parseText(tokenizedItem, original):
    #Looking for names
    name = []
    unit = ""
    amount = []
    unit = [item[0] for item in tokenizedItem if re.search(measure_regex, item[0], flags=re.I)]
    for item in tokenizedItem:
        #Checking to find any food words
        if (item[1] == "NN" or item[1] == "NNS"  or item[1] == "NNP") and not re.search(measure_regex, item[0], flags=re.I):
            name.append(item[0])
        #Searches for numerical values
        #numSearch = re.findall(r'\d+', item[0], flags=re.I)
    numSearch = re.search(r"((\d+)\s*[\u00BC-\u00BE\u2150-\u215E])|[\u00BC-\u00BE\u2150-\u215E]|(\d+)", original, flags=re.I)
    if numSearch:
        amount = numSearch.group(0)       
    name = " ".join(name)
    
    return name, unit, amount

def parseToolsMethods(tokenizedItem):
    tools = []
    methods = []
    tools = (re.findall(tool_indicator_regex, tokenizedItem, flags=re.I))
    methods = (re.findall(method_indicator_regex, tokenizedItem, flags=re.I))
    return tools, methods

def main():
    totIng = []
    totTools = []
    totMethods = []
    page = "https://www.allrecipes.com/recipe/216032/apple-cider-stew/"
    ingredients, directions = urlScraper(page)
    for item in ingredients:
        parsedIng = pos_tag(word_tokenize(item))
        name, unit, amount = parseText(parsedIng, item)
        totIng.append(Ingredient(name, unit, amount))
    for item in directions:
        parsedDir = item
        tools, methods = parseToolsMethods(parsedDir)
        totTools += tools
        totMethods += methods
    for item in totIng:
        print("Name: " + item.name)
        print("Unit: " + str(item.unit))
        print("Amount: " + str(item.quantity))
        print('\n')
    print("Tools: " + str(set(totTools)))
    print("Methods: " + str(set(totMethods)))

if __name__ == '__main__':
    main()
