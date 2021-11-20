from IngredientParser import getRecipe
from healthy import transform_healthy

def main(): 
    print("Please Enter the URL for Recipe: ")
    page = input()
    print("What do you want to do with this recipe?\n")
    print("Enter 1 for viewing recipe.\n")
    print("Enter 2 for tranforming to healthy option.\n")
    print("Enter 3 for transforming to vegetarian option.\n")
    option = int(input())
    if option == 1:
        getRecipe(page)
    elif option == 2: 
        transform_healthy(page)

if __name__ == '__main__':
    main()