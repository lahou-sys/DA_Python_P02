import requests
from bs4 import BeautifulSoup

url = "http://books.toscrape.com/"

reponse = requests.get(url)

soup = BeautifulSoup(reponse.text, "html.parser")

categories = []
categorie = soup.find("div", class_="side_categories")
#print(categorie)
cat = categorie.findChildren("a", recursive=True)
#print(cat)

for i in cat:
    a = ((i.contents[0]).rstrip("\n")).strip()
    categories.append(a)


# categorie2 = categorie.findAll("ul", class_="nav nav-list")
# liste_cat = categorie2.find_all("ul", text=None)
# #cat = categorie.find('lu')

# print(liste_cat.text)

""" for lu in categorie2:
    for li in ul.find('ul'):
        d = li.find('a')
        print(d)
        #e = d['href']
        #categories.append(str(e)) """
        

""" for i in cat:
    #c = i.find('li')
    d = i.find('a')
    #d = (c.replace(" ", "")).replace("\n", "")
    categories.append(d) """

a = "http://books.toscrape.com/catalogue/category/books/travel_2/index.html"

b = a.split("/")[-5]

print(b)

