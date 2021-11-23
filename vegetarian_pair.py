def txtToList(txtfile):
    meats = []
    #txt = open(txtfile, 'r')
    txt= open(txtfile, encoding='utf-8')
    for line in txt:
        meats.append(line.strip())
    return meats


meats = txtToList('foods/meats.txt')
seafood = txtToList('foods/seafood.txt')
meat_sauces = [
    'anchovy essence',
    'duck sauce',
    'gravy',
    'bolognese',
    'picadillo',
    'ragu',
    'lobster sauce',
    'fish sauce',
    'pla ra',
    'sauce espagnole',
    'espagnole sauce',
    'genovese sauce',
    'neapolitan ragu',
    'ragu alla salsiccia',
    'cincalok',
    'liver sauce',
    'grey polish sauce',
    "hunter's sauce",
    'skagen sauce',
    'worcestershire sauce',
    'shrimp paste',
    'fish paste',
    'anchovy paste',
    'liver spread',
    'lechon sauce'
]

protein_subs = [
    'tofu',
    'tempeh',
    'jackfruit'
    'seitan',
    'beyond meat',
]

all_non_veg = meats + seafood + meat_sauces

vegetables = txtToList('foods/vegetables.txt')


vegetarian_nonvegetarian = [
    {
        'vegetarian': 'tofu', 
        'non_vegetarian': meats
    },
    {
        'vegetarian': 'tempeh', 
        'non_vegetarian': seafood
    },
    {
        'vegetarian': 'tomato sauce', 
        'non_vegetarian': meat_sauces
    }
]

#for dictio in vegetarian_nonvegetarian:
#    for key, val in dictio.items():
#        print(key, ': ', val)