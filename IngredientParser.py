from json import detect_encoding
from nltk import word_tokenize, pos_tag, RegexpParser
from pageScraper import urlScraper
import re
measure_regex = '(cup|spoon|fluid|ounce|pinch|gill|pint|quart|gallon|pound|drops|recipe|slices|pods|package|can|head|halves|stalk)'
tool_indicator_regex = '(pan|skillet|pot|sheet|grate|whisk|griddle|bowl|oven|dish)'
method_indicator_regex = '(boil|bake|baking|simmer|stir|roast|fry|combine|heat|microwave|add)'
time_indicator_regex = '(min|hour)'
with open("foods/sauces.txt", encoding='utf-8') as f:
    sauce_list = f.read().splitlines()
with open("foods/dairy.txt", encoding='utf-8') as f:
    dairy_list = f.read().splitlines()
with open("foods/fruits.txt", encoding='utf-8') as f:
    fruits_list = f.read().splitlines()
with open("foods/grains.txt", encoding='utf-8') as f:
    grains_list = f.read().splitlines()
with open("foods/meats.txt", encoding='utf-8') as f:
    meats_list = f.read().splitlines()
with open("foods/seafood.txt", encoding='utf-8') as f:
    seafood_list = f.read().splitlines()
with open("foods/vegetables.txt", encoding='utf-8') as f:
    vegetables_list = f.read().splitlines()
with open("foods/spices.txt", encoding='utf-8') as f:
    spices_list = f.read().splitlines()

class Ingredient:
    def __init__(self, name, unit, quantity=None, preperation=None):
        self.name = name
        self.quantity = quantity
        self.unit = unit
        self.preperation = preperation
        self.type = categorize(self)
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

def categorize(self):
    # special cases:
    if self.name.lower().find('sauce') >= 0: return 'S'
    # normal execution:
    types = ''
    if any(set(self.name.strip().split(' ')).intersection(set(example.lower().split(' '))) for example in spices_list) and len(types) ==0: types = 'H'
    
    if any(set(self.name.strip().split(' ')).intersection(set(example.lower().split(' '))) for example in meats_list) and len(types) ==0: types ='M' 
    if any(set(self.name.strip().split(' ')).intersection(set(example.lower().split(' '))) for example in vegetables_list) and len(types) ==0: types = 'V'
    if any(set(self.name.strip().split(' ')).intersection(set(example.lower().split(' '))) for example in dairy_list) and len(types) ==0: types = 'D' 
    if any(set(self.name.strip().split(' ')).intersection(set(example.lower().split(' '))) for example in grains_list) and len(types) ==0: types = 'G'
    if any(set(self.name.strip().split(' ')).intersection(set(example.lower().split(' '))) for example in grains_list) and len(types) ==0: types = 'G'
    if any(set(self.name.strip().split(' ')).intersection(set(example.lower().split(' '))) for example in sauce_list) and len(types) ==0: types = 'S'
    if any(set(self.name.strip().split(' ')).intersection(set(example.lower().split(' '))) for example in seafood_list) and len(types) ==0: types = 'P'
    if any(set(self.name.strip().split(' ')).intersection(set(example.lower().split(' '))) for example in fruits_list) and len(types) ==0: types = 'F' 
    if len(types) == 0: types = '?'
    return types
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
    else:
        amount = ""
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

class Step:
    def __init__(self, instruction, ingredients):
        res = parseToolsMethods(instruction)
        self.tools = res[0]
        self.ingredients = self.findIng(instruction, ingredients)
        self.methods = res[1]
        self.time = self.findTime(instruction)
    
    def findIng(self, instruction, ingredients):
        name = []
        parsedInstr = (word_tokenize(instruction))
        tot = []
        for i, inst in enumerate(parsedInstr):
            #creates a list of all ingredient names the current instruction word appears in
            temp = [x.name for x in ingredients if inst in x.name and len(inst)>2]
            temp = set(temp)
            #Designed to catch things that share one word (eg apple cider versus Fuji apple)
            #Tries to ensure we only add one item for each word max
            if len(temp)>=2 and i+1 < len(parsedInstr):
                bef = " ".join([parsedInstr[i-1], inst])
                aft = " ".join([inst, parsedInstr[i+1]])
                beforeCheck = [x.name for x in ingredients if bef in x.name]
                afterCheck = [x.name for x in ingredients if aft in x.name]
                if beforeCheck:
                    temp = beforeCheck
                elif afterCheck:
                    temp = afterCheck
                else:
                    bef = bef.split(" ")
                    aft = aft.split(" ")
                    befCheck1 = [x.name for x in ingredients if bef[0] in x.name]
                    aftCheck2 = [x.name for x in ingredients if aft[1] in x.name]
                    if len(befCheck1) > 0:
                        temp = befCheck1
                    elif len(aftCheck2) > 0:
                        temp = aftCheck2
            tot += temp
        return set(tot)
    
    def findTime(self, instruction):
        tokenTime = word_tokenize(instruction)
        hours = 0
        minutes = 0
        for i,item in enumerate(tokenTime):
            if re.search('(hour)', item):
                hours += int(tokenTime[i-1])
            if re.search("min", item) and not re.search("alumin", item):
                minutes += int(tokenTime[i-1])
        if hours == 0:
            return minutes
        else:
            return (hours * 60) + minutes

def parseSteps(url, totIng):
    totSteps = []
    ingredients, directions = urlScraper(url)
    for dir in directions:
        dir = re.sub(" +", " ",dir)
        dir = dir.strip()
        currList = []
        totSteps.append(currList)
        head = currList
        broken = dir.split('.')
        newItem = []
        for item in broken:
            newItem += item.split(";")
        broken = newItem
        for i, ind in enumerate(broken):
            test = Step(ind, totIng)
            if not test.tools and not test.methods and not test.ingredients:
                continue
            elif not (test.tools or test.methods or test.ingredients):
                y = [test]
                currList.append(y)
                currList = y
            else:
                currList = head
                currList.append(test)
                
    return totSteps

def totalToolsMethods(url):
    totTools = []
    totMethods = []
    page = url
    ingredients, directions = urlScraper(page)
    for dir in directions:
        dir = re.sub(" +", " ",dir)
        dir = dir.strip()
        tools = (re.findall(tool_indicator_regex, dir, flags=re.I))
        methods = (re.findall(method_indicator_regex, dir, flags=re.I))
        totTools += tools
        totMethods += methods

    return totMethods, totTools


def findAllIng(url):
    totIng = []
    page = url
    ingredients, directions = urlScraper(page)
    for item in ingredients:
        grammar = r"CHUNK: {<JJ>*<NN|NNS|NNP>}"
        name, unit, amount, preperation = parseTextChunk(item, grammar)
        # parsedIng = pos_tag(word_tokenize(item))
        # name, unit, amount = parseText(parsedIng, item)
        totIng.append(Ingredient(name, unit, amount, preperation))
    return totIng

class Recipe:
    def __init__(self, url):
        temp = findAllIng(url)
        self.ingredients = temp
        tm = totalToolsMethods(url)
        self.tools = tm[1]
        self.methods = tm[0]
        self.instructions = parseSteps(url, temp)
    


def main():
    totIng = []
    totTools = []
    totMethods = []
    page = "https://www.allrecipes.com/recipe/267015/pakistani-ground-beef-curry/"
    ingredients, directions = urlScraper(page)
    for item in ingredients:
        grammar = r"CHUNK: {<JJ>*<NN|NNS|NNP>}"
        name, unit, amount, preperation = parseTextChunk(item, grammar)
        # parsedIng = pos_tag(word_tokenize(item))
        # name, unit, amount = parseText(parsedIng, item)
        totIng.append(Ingredient(name, unit, amount, preperation))
    t = Recipe(page)
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
