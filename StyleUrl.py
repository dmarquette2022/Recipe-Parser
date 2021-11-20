import bs4 as bs
import urllib.request
from IngredientParser import Recipe, Ingredient
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from VoteSystem import voteCounter, sortVote

import re
import time


def gatherURLs():
    totUrl = []
    page ="https://www.allrecipes.com/recipes/233/world-cuisine/asian/indian/"
    options = Options()
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--headless')
    options.page_load_strategy = 'normal'
    caps = DesiredCapabilities().CHROME
    caps["pageLoadStrategy"] = "eager"  #  complete
    driver = webdriver.Chrome(desired_capabilities=caps, executable_path="driver/chromedriver", chrome_options=options)
    driver.get(page)
    element = driver.find_element_by_id("category-page-list-related-load-more-button")
    for i in range(10):
        element.click()
        driver.implicitly_wait(3)
    html = driver.page_source
    soup = bs.BeautifulSoup(html, "lxml")
    tempSoup = soup
    soup = soup.find_all("a", {"class":"card__titleLink manual-link-behavior"})
    for item in soup:
        if not re.search("gallery", item['href']): totUrl.append(item['href'])
    soup = tempSoup.find_all("a", {"class":"recipeCard__titleLink"})
    for item in soup:
        if not re.search("gallery", item['href']): totUrl.append(item['href'])
    return set(totUrl)

def gatherIngredients():
    totUrls =  gatherURLs()
    totIng = {}
    for url in totUrls:
        t = Recipe(url)
        for ing in t.ingredients:
            if ing.type in totIng:
                if ing.name in totIng[ing.type]:
                    totIng[ing.type][ing.name] += 1
                else:
                    totIng[ing.type][ing.name] = 1
            else:
                totIng[ing.type] = {ing.name:1}
    for type in totIng:
        totIng[type] = sortVote(totIng[type])
    return totIng


def main():
    t = gatherIngredients()
    print(t)


if __name__ ==  '__main__':
    main()

    





