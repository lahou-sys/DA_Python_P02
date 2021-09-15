# -*- coding: utf8 -*-


import csv
import math
import os
import threading
import time
import urllib.request
from urllib.parse import urljoin
from concurrent.futures import ThreadPoolExecutor, as_completed
import requests
from bs4 import BeautifulSoup


def mkdir_directory(directory):
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
    soup = make_soup(url)
    categories_liste = []
    categorie_side = soup.find("div", class_="side_categories")
    cacategories = categorie_side.findChildren("a")
    for i in cacategories:
        item = ((i.contents[0]).rstrip("\n")).strip()
        categories_liste.append(item)
    return categories_liste


def liste_url_categories(url):
    soup = make_soup(url)
    categories_liste_url = []
    categorie_side = soup.find("div", class_="side_categories")
    cacategories = categorie_side.findChildren("a")
    for i in cacategories:
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
    soup = make_soup(url_categorie)
    if not soup.find("li", class_="next"):
        liste_book_of_categorie= soup.find("ol", class_="row")
        url_book = liste_book_of_categorie.findChildren("h3")
        for i in url_book:
            url_b = i.find("a")
            item = url_build(url_categorie,url_b)
            book_liste_url.append(item)
    else:
        page = 0
        next_test = soup.find("li", class_="next")
        while next_test:
            page += 1
            p = "page-" + str(page) + ".html"
            url_page = url_categorie.replace("index.html", p )
            soup = make_soup(url_page)
            liste_book_of_categorie= soup.find("ol", class_="row")
            url_book = liste_book_of_categorie.findChildren("h3")
            for i in url_book:
                url_b = i.find("a")
                item = url_build(url_categorie,url_b)
                book_liste_url.append(item)
            next_test = soup.find("li", class_="next")       
    return book_liste_url


def list_url_book_categorie_pool(url, categorie):
    book_liste_url = []
    next_page = False
    url_categorie = dic_categories_url(url)[categorie]
    soup = make_soup(url_categorie)
    if not soup.find("li", class_="next"):
        liste_book_of_categorie= soup.find("ol", class_="row")
        url_book = liste_book_of_categorie.findChildren("h3")
        for i in url_book:
            url_b = i.find("a")
            item = url_build(url_categorie,url_b)
            book_liste_url.append(item)
    else:
        page = 0
        next_test = soup.find("li", class_="next")
        while next_test:
            page += 1
            p = "page-" + str(page) + ".html"
            url_page = url_categorie.replace("index.html", p )
            soup = make_soup(url_page)
            liste_book_of_categorie= soup.find("ol", class_="row")
            url_book = liste_book_of_categorie.findChildren("h3")
            for i in url_book:
                url_b = i.find("a")
                item = url_build(url_categorie,url_b)
                book_liste_url.append(item)
            next_test = soup.find("li", class_="next")       
    return book_liste_url


def extract_attributs_book(url):
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


def extract_upc(url):
    upc = extract_attributs_book(url)['UPC']
    return upc


def extract_title(url):
    soup = make_soup(url)
    section = soup.find("div", attrs={"class": "col-sm-6 product_main"})
    title = section.find("h1")
    return title.text


def extract_categorie(url):
    soup = make_soup(url)
    section = soup.find("div", attrs={"class": "container-fluid page"})
    section_2 = section.find("ul", attrs={"class": "breadcrumb"} )
    liste_item = []
    for i in section_2.find_all("li"):
        i = (i.text).replace("\n","")
        liste_item.append(i)
    categorie = liste_item[2]
    return categorie


def extract_price_including_tax(url):
    price_including_tax = extract_attributs_book(url)['Price (incl. tax)']
    return price_including_tax.replace("Â", "")


def extract_price_excluding_tax(url):
    price_excluding_tax = extract_attributs_book(url)['Price (excl. tax)']
    return price_excluding_tax.replace("Â", "")


def extract_number_available(url):
    number_available = extract_attributs_book(url)['Availability']
    return (number_available.replace("In stock (", "")).replace("available)", "")


def extract_product_description(url):
    soup = make_soup(url)
    section = soup.find("div", attrs={"id": "content_inner"})
    if section.find("p", attrs=None):
        product_description = (section.find("p", attrs=None).text).replace(",", "")
        return product_description
    else:
        return None


def extract_review_rating(url):
    notes = ("One", "Two", "Three", "Four", "Five" )
    review_rating = "None"
    soup = make_soup(url)
    section = soup.find("div", attrs={"class": "col-sm-6 product_main"})
    for n in notes:
        note = "star-rating " + n
        if section.find("p", attrs={"class": note}):
            review_rating = n     
    return review_rating


def extract_image_url(url):
    soup = make_soup(url)
    section = soup.find("div", attrs={"class": "item active"})
    image_url = section.find("img")["src"]
    return url_src_build(url,image_url)


""" def extract_all_book_of_categorie(url, categorie):
    liste_url_books = list_url_book_categorie(url, categorie)
    liste_books = []
    for i in liste_url_books:
        books = {}
        books["product_page_url"] = i
        books["universal_ product_code (upc)"] = extract_upc(i)
        books["title"] = extract_title(i)
        books["price_including_taxe"] = extract_price_including_tax(i)
        books["price_excluding_taxe"] = extract_price_excluding_tax(i)
        books["number_available"] = extract_number_available(i)
        books["product_description"] = extract_product_description(i)
        books["category"] = extract_categorie(i)
        books["review_rating"] = extract_review_rating(i)
        books["image_url"] = extract_image_url(i)   
        liste_books.append(books)
    return liste_books """

def chunks_liste(l, n):
    last = 0
    for i in range(1, n+1):
        cur = int(round(i * (len(l) / n)))
        yield l[last:cur]
        last = cur


def extract_infos_books(liste_url):
    i = liste_url
    books = {}
    books["product_page_url"] = i
    books["universal_ product_code (upc)"] = extract_upc(i)
    books["title"] = extract_title(i)
    books["price_including_taxe"] = extract_price_including_tax(i)
    books["price_excluding_taxe"] = extract_price_excluding_tax(i)
    books["number_available"] = extract_number_available(i)
    books["product_description"] = extract_product_description(i)
    books["category"] = extract_categorie(i)
    books["review_rating"] = extract_review_rating(i)
    books["image_url"] = extract_image_url(i)
    return books 
        

def extract_all_book_of_categoriePool(url, categorie):
    liste_url_books = list_url_book_categorie(url, categorie)
    nombre_books = len(liste_url_books)
    nombre_max_url = 100
    print(nombre_books)
    taille_sous_liste = math.ceil(nombre_books / nombre_max_url)
    print(taille_sous_liste)
    liste_url_books_divise = list(chunks_liste(liste_url_books, taille_sous_liste))
    print(len(liste_url_books_divise))
    liste_books = []
    processes = []
    for i in liste_url_books_divise:
        with ThreadPoolExecutor(max_workers=100) as executor:
            for j in i:
                result = processes.append(executor.submit(extract_infos_books, j))          
    for task in as_completed(processes):
        liste_books.append(task.result())
    return liste_books


def export_to_csv(url,categorie):
    books = extract_all_book_of_categoriePool(url, categorie)
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


""" def download_all_pictures(url,categorie):
    directory = "pictures_" + categorie +"_"+ time.strftime("%y%m%d%H%M%S")
    mkdir_directory(directory)
    liste_url_books = list_url_book_categorie(url, categorie)
    liste_books = []
    for i in liste_url_books:
        books = {}
        books["universal_ product_code (upc)"] = extract_upc(i)
        books["image_url"] = extract_image_url(i)   
        liste_books.append(books)
    for j in liste_books:
        liste_item = []
        for key, value in j.items():
            liste_item.append(value)
        name_picture = "pictures_" + categorie +"_"+"upc-" + liste_item[0] + ".jpg"
        fullfilename = os.path.join(directory, name_picture)
        urllib.request.urlretrieve(liste_item[1],fullfilename)
 """

""" def download_all_pictures_pool_old(url,categorie):
    directory = "pictures_" + categorie +"_"+ time.strftime("%y%m%d%H%M%S")
    mkdir_directory(directory)
    books = extract_all_book_of_categoriePool(url, categorie)
    liste_books = []
    for i in range(len(books)):
        key_to_extract = {"universal_ product_code (upc)", "image_url"}
        dic = books[i]
        new_dic = {key: dic[key] for key in dic.keys() & key_to_extract}
        liste_books.append(new_dic)
    for j in liste_books:
        liste_item = []
        for key, value in j.items():
            liste_item.append(value)
        name_picture = "pictures_" + categorie +"_"+"upc-" + liste_item[0] + ".jpg"
        fullfilename = os.path.join(directory, str(name_picture))
        urllib.request.urlretrieve(liste_item[1],fullfilename) """

def download_all_pictures_pool(url,categorie):
    directory = "pictures_" + categorie +"_"+ time.strftime("%y%m%d%H%M%S")
    mkdir_directory(directory)
    books = extract_all_book_of_categoriePool(url, categorie)
    liste_books = []
    for i in range(len(books)):
        key_to_extract = {"universal_ product_code (upc)", "image_url"}
        dic = books[i]
        new_dic = {key: dic[key] for key in dic.keys() & key_to_extract}
        new_dic = dict(sorted(new_dic.items()))
        liste_books.append(new_dic)
    book_url = []
    book_fullfilename = []
    liste_item = []
    for j in liste_books:
        for key in j:
            liste_item.append(j[key])
        name_picture = "pictures_" + categorie +"_"+"upc-" + liste_item[1] + ".jpg"
        fullfilename = os.path.join(directory, str(name_picture))
        url = liste_item[0]
        book_url.append(url)
        book_fullfilename.append(str(fullfilename))
        liste_item = []
    threads = []
    for i in range(2):
        for u,f in zip(book_url, book_fullfilename):
            thread = threading.Thread(target=download_picture_url_pool, args=(u,f))
            threads.append(thread)
            thread.start()
    for i in threads:
        i.join()
    

def download_picture_url_pool(url,fullfilename):
    urllib.request.urlretrieve(url,fullfilename)



URL = "http://books.toscrape.com/"

start_time = time.time()

#print(len(list_url_book_categorie(URL, "Fiction")))

#print(list_url_book_categorie(URL, "Fiction"))

#print(export_to_csv(URL, "Travel"))

#print((list_url_book_categorie(URL, "Travel")))

#print(liste_url_categories(URL))

#print(liste_item_categories(URL))

#print(extract_product_description("http://books.toscrape.com/catalogue/starlark_56/index.html"))

#print(extract_all_book_of_categorie(URL, "Crime"))

export_to_csv(URL, "Travel")

#print(extract_categorie("http://books.toscrape.com/catalogue/starlark_56/index.html"))

#download_all_pictures(URL, "Books")

#print(list_url_book_categorie(URL, "Books"))

#print(extract_all_book_of_categoriePool(URL, "Religion"))
#print(len(extract_all_book_of_categoriePool(URL, "Religion")))

#download_all_pictures_pool(URL, "Travel")


print("--- %s seconds ---" % (time.time() - start_time))