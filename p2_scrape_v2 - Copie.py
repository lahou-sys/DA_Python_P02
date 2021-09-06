# -*- coding: utf8 -*-


#from re import T
#from typing import Text
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import urllib.request
import csv
import time
import os


def mkdirDirectory(directory):
    os.mkdir(directory)


def url_build(web_url, url_part):
    url_full = urljoin(web_url,url_part.get('href'))
    return url_full


def url_src_build(web_url, url_part):
    url_full = urljoin(web_url,url_part)
    return url_full

def make_soup(url):
    reponse = requests.get(url)
    soup = BeautifulSoup(reponse.text, "html.parser")
    return soup

def liste_item_categories(url):
    # reponse = requests.get(url)
    # soup = BeautifulSoup(reponse.text, "html.parser")
    soup = make_soup(url)
    categories_liste = []
    categorie_side = soup.find("div", class_="side_categories")
    cacategories = categorie_side.findChildren("a")
    for i in cacategories:
        item = ((i.contents[0]).rstrip("\n")).strip()
        categories_liste.append(item)
    return categories_liste


def liste_url_categories(url):
    #reponse = requests.get(url)
    #soup = BeautifulSoup(reponse.text, "html.parser")
    soup = make_soup(url)
    categories_liste_url = []
    categorie_side = soup.find("div", class_="side_categories")
    cacategories = categorie_side.findChildren("a")
    for i in cacategories:
        #item = ((i['href']).rstrip("\n")).strip()
        #print(item)
        item = url_build(url,i)
        categories_liste_url.append(item)
    return categories_liste_url


def dic_categories_url(url):
    key_list = liste_item_categories(url)
    value_list = liste_url_categories(url)
    dic_categories = dict(zip(key_list, value_list))
    return dic_categories

def list_url_book_categorie(url, categorie):
    book_liste_url = []
    next_page = False
    url_categorie = dic_categories_url(url)[categorie]
    #reponse = requests.get(url_categorie)
    #soup = BeautifulSoup(reponse.text, "html.parser")
    soup = make_soup(url_categorie)
    if not soup.find("li", class_="next"):
        liste_book_of_categorie= soup.find("ol", class_="row")
        url_book = liste_book_of_categorie.findChildren("h3")
        #print(url_book)
        #suffix_url = url_categorie.split("/")[-5]
        for i in url_book:
            url_b = i.find("a")
            #item = ((url_b['href']).replace("../../..", suffix_url))
            item = url_build(url_categorie,url_b)
            book_liste_url.append(item)
    else:
        page = 0
        next_test = soup.find("li", class_="next")
        while next_test:
            page += 1
            p = "page-" + str(page) + ".html"
            url_page = url_categorie.replace("index.html", p )
            #reponse_p = requests.get(url_page)
            #soup_p = BeautifulSoup(reponse_p.text, "html.parser")
            soup = make_soup(url_page)
            liste_book_of_categorie= soup.find("ol", class_="row")
            url_book = liste_book_of_categorie.findChildren("h3")
            #suffix_url = url_categorie.split("/")[-5]
            for i in url_book:
                url_b = i.find("a")
                #item = ((url_b['href']).replace("../../..", suffix_url))
                item = url_build(url_categorie,url_b)
                book_liste_url.append(item)
            next_test = soup.find("li", class_="next")       
    return book_liste_url


def extractAttributsBook(url):
    soup = make_soup(url)
    section = soup.find("table", attrs={"class": "table table-striped"})
    tables = section.find_all("tr")
    table_header = []
    table_data = []
    for i in tables:
        header = i.find("th")
        table_header.append(header.text)
        data_row = i.find("td")
        table_data.append(data_row.text)
    dic_attributs_book = dict(zip(table_header, table_data))
    return dic_attributs_book

def extractUpc(url):
    upc = extractAttributsBook(url)['UPC']
    return upc


def extractTitle(url):
    soup = make_soup(url)
    section = soup.find("div", attrs={"class": "col-sm-6 product_main"})
    title = section.find("h1")
    return title.text

def extractCategorie(url):
    soup = make_soup(url)
    section = soup.find("div", attrs={"class": "container-fluid page"})
    section_2 = section.find("ul", attrs={"class": "breadcrumb"} )
    liste_item = []
    for i in section_2.find_all("li"):
        i = (i.text).replace("\n","")
        liste_item.append(i)
    categorie = liste_item[2]
    return categorie


def extractPriceIncludingTax(url):
    price_including_tax = extractAttributsBook(url)['Price (incl. tax)']
    return price_including_tax.replace("Â", "")


def extractPriceExcludingTax(url):
    price_excluding_tax = extractAttributsBook(url)['Price (excl. tax)']
    return price_excluding_tax.replace("Â", "")


def extractNumberAvailable(url):
    number_available = extractAttributsBook(url)['Availability']
    return (number_available.replace("In stock (", "")).replace("available)", "")


def extractProductDescription(url):
    soup = make_soup(url)
    section = soup.find("div", attrs={"id": "content_inner"})
    if section.find("p", attrs=None):
        product_description = (section.find("p", attrs=None).text).replace(",", "")
        return product_description
    else:
        return None


def extractReviewRating(url):
    notes = ("One", "Two", "Three", "Four", "Five" )
    review_rating = "None"
    soup = make_soup(url)
    section = soup.find("div", attrs={"class": "col-sm-6 product_main"})
    for n in notes:
        note = "star-rating " + n
        if section.find("p", attrs={"class": note}):
            review_rating = n     
    return review_rating


def extractImageUrl(url):
    soup = make_soup(url)
    section = soup.find("div", attrs={"class": "item active"})
    image_url = section.find("img")["src"]
    return url_src_build(url,image_url)

def extractAllBookOfCategorie(url, categorie):
    liste_url_books = list_url_book_categorie(url, categorie)
    liste_books = []
    for i in liste_url_books:
        books = {}
        books["product_page_url"] = i
        books["universal_ product_code (upc)"] = extractUpc(i)
        books["title"] = extractTitle(i)
        books["price_including_taxe"] = extractPriceIncludingTax(i)
        books["price_excluding_taxe"] = extractPriceExcludingTax(i)
        books["number_available"] = extractNumberAvailable(i)
        books["product_description"] = extractProductDescription(i)
        books["category"] = extractCategorie(i)
        books["review_rating"] = extractReviewRating(i)
        books["image_url"] = extractImageUrl(i)   
        liste_books.append(books)
    return liste_books


def exportToCsv(url,categorie):
    start_time = time.time()
    books = extractAllBookOfCategorie(url, categorie)
    header_list = []
    for key in books[0]:
        header_list.append(key)
    with open("output.csv", "w", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile, delimiter=',')
        writer.writerow(header_list)      
        for i in books:
            liste_item = []
            for key, value in i.items():
                liste_item.append(value)
            writer.writerow(liste_item)
        print("--- %s seconds ---" % (time.time() - start_time))


def downloadAllPictures(url,categorie):
    start_time = time.time()
    directory = "pictures_" + categorie +"_"+ time.strftime("%y%m%d%H%M%S")
    mkdirDirectory(directory)
    liste_url_books = list_url_book_categorie(url, categorie)
    liste_books = []
    for i in liste_url_books:
        books = {}
        books["universal_ product_code (upc)"] = extractUpc(i)
        books["image_url"] = extractImageUrl(i)   
        liste_books.append(books)
    for j in liste_books:
        liste_item = []
        for key, value in j.items():
            liste_item.append(value)
        name_picture = "pictures_" + categorie +"_"+"upc-" + liste_item[0] + ".jpg"
        fullfilename = os.path.join(directory, name_picture)
        urllib.request.urlretrieve(liste_item[1],fullfilename)
    print("--- %s seconds ---" % (time.time() - start_time))





    
    """ url_categorie = dic_categories_url(url)[categorie]
    reponse = requests.get(url_categorie)
    soup = BeautifulSoup(reponse.text, "html.parser")
    
    liste_book_of_categorie= soup.find("ol", class_="row")
    url_book = liste_book_of_categorie.findChildren("a")
    suffix_url = url_categorie.split("/")[-5]
    for i in url_book:
        item = ((i['href']).replace("../../..", suffix_url))
        book_liste_url.append(url + item)
    return book_liste_url """




URL = "http://books.toscrape.com/"



#print(len(list_url_book_categorie(URL, "Fiction")))

#print(list_url_book_categorie(URL, "Fiction"))

#print(exportToCsv(URL, "Travel"))

#print((list_url_book_categorie(URL, "Travel")))

#print(liste_url_categories(URL))

#print(liste_item_categories(URL))

#print(extractProductDescription("http://books.toscrape.com/catalogue/starlark_56/index.html"))

#print(extractAllBookOfCategorie(URL, "Crime"))

print(exportToCsv(URL, "Books"))

#print(extractCategorie("http://books.toscrape.com/catalogue/starlark_56/index.html"))

#downloadAllPictures(URL, "Books")
