import bs4 as bs
import urllib.request

def urlScraper(page):
    ingredients = []
    instructions = []
    source = urllib.request.urlopen(page).read()
    soup = bs.BeautifulSoup(source,'lxml')
    htmlIngredients = soup.find_all('span', {'class': "ingredients-item-name"})
    for item in htmlIngredients:
        ingredients.append(item.text)
    htmlInstructions = soup.find('ul', {'class':'instructions-section'})
    # for item in htmlInstructions.find_all('li'):
    for item in htmlInstructions.find_all('p'):
        instructions.append(item.text)
    return ingredients, instructions

def main():
    page = "https://www.allrecipes.com/recipe/234592/buffalo-chicken-stuffed-shells/"
    print(urlScraper(page))

if __name__ == '__main__':
    main()
