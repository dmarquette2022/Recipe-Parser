from vegetarian_pair import txtToList

cheese = txtToList('foods/cheese.txt')
milk = [
    'milk',
    'whole milk',
    'skim milk',
    'low-fat milk',
    'goat milk',
    'sheep milk',
    'cow milk',
    'buttermilk'
    ]
butter = [
    'butter',
    'ghee'
]
yogurt = [
    'yogurt',
    'greek yogurt',
    'low-fat yogurt',
    'goat milk yogurt',
    "sheep's milk yogurt",
    'sheep milk yogurt',
]
cream = [
    'cream',
    'half and half',
    'half & half',
    'whipped cream',
    'whipping cream',
    'sour cream',
    'heavy cream',
    'light cream',
    'clotted cream',
    'pure cream'
]
ice_cream = [
    'ice cream',
    'gelato',
    'sherbet'
    ]
protein = [
    'casein',
    'casein protein'
    'whey',
    'whey protein'
]




lactosefree_lactose = [
    {
        'lactose-free': 'almond cheese', 
        'lactose': cheese
    },
    {
        'lactose-free': 'almond milk', 
        'lactose': milk
    },
    {
        'lactose-free': 'margarine', 
        'lactose': butter
    },
    {
        'lactose-free': 'coconut milk yogurt', 
        'lactose': yogurt
    },
    {
        'lactose-free': 'coconut cream', 
        'lactose': cream
    },
    {
        'lactose-free': 'dairy-free ice cream', 
        'lactose': ice_cream
    },
    {
        'lactose-free': 'vegan protein powder', 
        'lactose': protein
    },
]
