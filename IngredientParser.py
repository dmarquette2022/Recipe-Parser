from nltk import word_tokenize, pos_tag, RegexpParser
from pageScraper import urlScraper
import re
measure_regex = '(cup|spoon|fluid|ounce|pinch|gill|pint|quart|gallon|pound|drops|recipe|slices|pods|package|can|head|halves|stalk)'
tool_indicator_regex = '(pan|skillet|pot|sheet|grate|whisk|griddle|bowl|oven|dish)'
method_indicator_regex = '(boil|bake|baking|simmer|stir|roast|fry)'
time_indicator_regex = '(min|hour)'

class Ingredient:
    def __init__(self, name, unit, quantity=None, preperation=None):
        self.name = name
        self.quantity = quantity
        self.unit = unit
        self.preperation = preperation
#with nltk tokenization     
def parseText(tokenizedItem, original):
    #Looking for names
    name = []
    unit = ""
    amount = []
    unit = [item[0] for item in tokenizedItem if re.search(measure_regex, item[0], flags=re.I)]
    for item in tokenizedItem:
        #Checking to find any food words
        if (item[1] == "NN" or item[1] == "NNS" or item[1] == "NNP") and not re.search(measure_regex, item[0], flags=re.I):
            name.append(item[0])
        #Searches for numerical values
        #numSearch = re.findall(r'\d+', item[0], flags=re.I)
    numSearch = re.search(r"((\d+)\s*[\u00BC-\u00BE\u2150-\u215E])|[\u00BC-\u00BE\u2150-\u215E]|(\d+)", original, flags=re.I)
    if numSearch:
        amount = numSearch.group(0)       
    name = " ".join(name)
    
    return name, unit, amount

#with nltk chunk 
def parseTextChunk(sentence, grammar): 
    cp = RegexpParser(grammar)
    splits = sentence.split(',')
    parsedIng = pos_tag(word_tokenize(splits[0]))
    #get unit 
    unit = [item[0] for item in parsedIng if re.search(measure_regex, item[0], flags=re.I)]
    #get numeric measurement
    numSearch = re.search(r"((\d+)\s*[\u00BC-\u00BE\u2150-\u215E])|[\u00BC-\u00BE\u2150-\u215E]|(\d+)", sentence, flags=re.I)
    if numSearch:
        amount = numSearch.group(0)  
    chunked = cp.parse(parsedIng)
    #get Ingredient name
    name = []
    for subtree in chunked.subtrees(): 
        if subtree.label() == "CHUNK": 
            words = [leaf[0] for leaf in subtree.leaves() if leaf[0] not in unit and leaf[0] not in amount and leaf[0] != 'Optional']
            phrase = " ".join(words)
            name.append(phrase)
    name = " ".join(name)
    #get preparation if available
    preperation = []
    if len(splits) > 1:
        g = r"CHUNK: {<JJ>*<IN>*<VBN|VBD|NN|NNS|NNP>}"
        prepCP = RegexpParser(g)
        for i in range(1, len(splits)):
            parsedPrep = pos_tag(word_tokenize(splits[i]))
            print(parsedPrep)
            chunked = prepCP.parse(parsedPrep)
            for subtree in chunked.subtrees(): 
                if subtree.label() == "CHUNK": 
                    words = [leaf[0] for leaf in subtree.leaves() if leaf[0] != "Optional"]
                    phrase = " ".join(words)
                    preperation.append(phrase)
            # curr = [item[0] for item in parsedPrep if item[1] in ['VBN', 'VBD', ''] and item[0] != 'Optional']
            # for c in curr: 
            #     preperation.append(c)
    return name, unit, amount, preperation

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
        grammar = r"CHUNK: {<JJ>*<NN|NNS|NNP>}"
        name, unit, amount, preperation = parseTextChunk(item, grammar)
        # parsedIng = pos_tag(word_tokenize(item))
        # name, unit, amount = parseText(parsedIng, item)
        totIng.append(Ingredient(name, unit, amount, preperation))
    for item in directions:
        parsedDir = item
        tools, methods = parseToolsMethods(parsedDir)
        totTools += tools
        totMethods += methods
    for item in totIng:
        print("Name: " + item.name)
        print("Unit: " + str(item.unit))
        print("Amount: " + str(item.quantity))
        print("Preperation: " + str(item.preperation))
        print('\n')
    print("Tools: " + str(set(totTools)))
    print("Methods: " + str(set(totMethods)))

if __name__ == '__main__':
    main()
