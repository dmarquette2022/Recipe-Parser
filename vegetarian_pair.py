def meatToList(txtfile):
    meats = []
    txt = open(txtfile, 'r')
    txt= open("foods/meats.txt", encoding='utf-8')
    for line in txt:
        meats.append(line.strip())
    return meats

vegetarian_nonvegetarian = [
    {
        'vegetarian': 'tofu', 
        'non_vegetarian': meatToList('foods/meats.txt')
    }
]

reduce_half = ['just_a _placeholder']

#for key, val in vegetarian_nonvegetarian[0].items():
#    print(key, ': ', val)