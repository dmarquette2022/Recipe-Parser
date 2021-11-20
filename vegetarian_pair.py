def txtToList(txtfile):
    meats = []
    #txt = open(txtfile, 'r')
    txt= open(txtfile, encoding='utf-8')
    for line in txt:
        meats.append(line.strip())
    return meats

vegetarian_nonvegetarian = [
    {
        'vegetarian': 'tofu', 
        'non_vegetarian': txtToList('foods/meats.txt')
    },
    {
        'vegetarian': 'tempeh', 
        'non_vegetarian': txtToList('foods/seafood.txt')
    }
]

#for dictio in vegetarian_nonvegetarian:
#    for key, val in dictio.items():
#        print(key, ': ', val)