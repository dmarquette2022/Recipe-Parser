from IngredientParser import getRecipe
from healthy import transform_healthy
from vegetarian import transform_vegetarian, transform_from_vegetarian
from StyleSwitch import IndianTransform
from doublehalf import double_half
from lactosefree import transform_lactosefree

def main(): 
    while True: 
        print("Please Enter the URL for Recipe: (enter q for quitting the program)")
        page = input()
        if page == 'q':
            break
        while True:
            print("What do you want to do with this recipe?\n")
            print("Enter 1 for viewing recipe.\n")
            print("Enter 2 for tranforming to healthy option.\n")
            print("Enter 3 for transforming to unhealthy option.\n")
            print("Enter 4 for transforming to vegetarian option.\n")
            print("Enter 5 for transforming to non-vegetarian option.\n")
            print("Enter 6 for transforming to an Indian Style option.\n")
            print("Enter 7 for transforming to lactose-free option.\n")
            print("Enter 8 for doubling the amount of the recipe.\n")
            print("Enter 9 for halving the amount of the recipe.\n")           
            print("Enter 0 to go back and either parse another recipe or quit.\n")
            option = int(input())
            if option == 1:
                getRecipe(page)
                print('\n\n')
            elif option == 2: 
                transform_healthy(page, 'to')
                print('\n\n')
            elif option == 3:
                transform_healthy(page, 'from')
                print('\n\n')
            elif option == 4:
                transform_vegetarian(page)
                print('\n\n')
            elif option == 5:
                transform_from_vegetarian(page)
                print('\n\n')
            elif option == 6:
                IndianTransform(page)
                print('\n\n')
            elif option == 7:
                transform_lactosefree(page)
                print('\n\n')
            elif option == 8:
                double_half(page, True)
                print('\n\n')
            elif option == 9: 
                double_half(page, False)
                print('\n\n')
            elif option == 0:
                break 
            else: 
                print("Please enter a valid number.")
        



if __name__ == '__main__':
    main()