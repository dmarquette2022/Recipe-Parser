from IngredientParser import getRecipe
from healthy import transform_healthy
from vegetarian import transform_vegetarian
from StyleSwitch import IndianTransform
from doublehalf import double_half

def main(): 
    print("Please Enter the URL for Recipe: ")
    page = input()
    print("What do you want to do with this recipe?\n")
    print("Enter 1 for viewing recipe.\n")
    print("Enter 2 for tranforming to healthy option.\n")
    print("Enter 3 for transforming to vegetarian option.\n")
    print("Enter 4 for transforming to an Indian Style option.\n")
    print("Enter 5 for doubling the amount of the recipe.\n")
    print("Enter 6 for halving the amount of the recipe.\n")
    option = int(input())
    if option == 1:
        getRecipe(page)
    elif option == 2: 
        transform_healthy(page)
    elif option == 3:
        transform_vegetarian(page)
    elif option == 4:
        IndianTransform(page)
    elif option == 5:
        double_half(page, True)
    elif option == 6: 
        double_half(page, False)



if __name__ == '__main__':
    main()