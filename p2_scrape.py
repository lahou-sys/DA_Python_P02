# -*- coding: utf8 -*-

'''
Author: Lahoucine BEN MOULAY

'''

"""
Ce script réalise une extraction d'informations à patir d'un site de vente de 
livres ("http://books.toscrape.com/") vers un fichier "csv" et par catégorie.
Il télécharge aussi les images relatives aux livres par catégorie.
A son lancement, il réalise l'extraction des informations pour toutes les catégories.
Une arborencence sera créée sur le disque dur pour stocker les informations par catégorie.

"""

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
    """Création d'un répertoire sur le filesystème.
        directory : nom du dossier à créer

	"""
    try:
        os.mkdir(directory)
    except PermissionError:
        print(f"Impossible de créer le dossier de trvail '{directory}' !")
        print("Problème de permissions sur le dossier parent.")
        exit()
    except:
        print(f"Impossible de créer le dossier de trvail '{directory}' !")
        print("Vérifier que vous pouvez créer des dossiers et des fichiers dans le dossier contenant ce script.")
        exit()


def url_build(web_url, url_part):
    """Construction de l'url absolue d'un attribut "href".
        web_url : url de la page en cours
        url_part : url relative

	"""
    url_full = urljoin(web_url,url_part.get('href'))
    return url_full


def url_src_build(web_url, url_part):
    """Construction de l'url absolue d'un attribut "src".
        web_url : url de la page en cours
        url_part : url relative

	"""
    url_full = urljoin(web_url,url_part)
    return url_full


def make_soup(url):
    """Extraction de la page html d'une url.
        url : url de la page à extraire

	"""
    try:
        reponse = requests.get(url)
    except:
        print (f"Problème d'accès à l'url : {url} ! \nVérifier votre connexion et relancer le traitement.")
        os._exit(1)
    soup = BeautifulSoup(reponse.content, "html.parser")
    return soup


def dic_categories_url(url):
    """Création du dictionnaire catégorie et son url respective.
        url : url du site à scraper

	"""
    soup = make_soup(url)
    categorie_side = soup.find("div", class_="side_categories")
    cacategories = categorie_side.findChildren("a")
    dic_categories = {((i.contents[0]).rstrip("\n")).strip():url_build(url,i) for i in cacategories }
    return dic_categories


def list_url_book_categorie(categorie, dic_cat):
    """Création de la liste des urls des livres pour une categorie.
        categorie : categorie des livres
        dic_cat : dictionnaire des catégories (catégorie et son url)

	"""
    book_liste_url = []
    url_categorie = dic_cat[categorie]
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
            p = (f"page-{page}.html")
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


def extract_attributs_book(soup):
    """Extraction des infos générales du livre vers un dictionnaire.
        soup : contenue html de la page du livre
        Infos extraites:
            - n° UPC
            - price_including_tax
            - price_excluding_tax
            - number_available

	"""
    section = soup.find("table", attrs={"class": "table table-striped"})
    tables = section.find_all("tr")
    dic_attributs_book = {(i.find("th")).text:(i.find("td")).text for i in tables}
    return dic_attributs_book


def extract_upc(soup):
    """Extraction du numero UPC du livre.
        soup : contenue html de la page du livre

	"""
    upc = extract_attributs_book(soup)['UPC']
    return upc


def extract_title(soup):
    """Extraction du titre du livre.
        soup : contenue html de la page du livre

	"""
    section = soup.find("div", attrs={"class": "col-sm-6 product_main"})
    title = section.find("h1")
    return title.text


def extract_categorie(soup):
    """Extraction de la categorie du livre.
        soup : contenue html de la page du livre

	"""
    section = soup.find("div", attrs={"class": "container-fluid page"})
    section_2 = section.find("ul", attrs={"class": "breadcrumb"} )
    liste_item = []
    for i in section_2.find_all("li"):
        i = (i.text).replace("\n","")
        liste_item.append(i)
    categorie = liste_item[2]
    return categorie


def extract_price_including_tax(soup):
    """Extraction du prix livre avec la taxe.
        soup : contenue html de la page du livre

	"""
    price_including_tax = extract_attributs_book(soup)['Price (incl. tax)']
    return price_including_tax


def extract_price_excluding_tax(soup):
    """Extraction du prix livre sans la taxe.
        soup : contenue html de la page du livre

	"""
    price_excluding_tax = extract_attributs_book(soup)['Price (excl. tax)']
    return price_excluding_tax


def extract_number_available(soup):
    """Extraction du nombre d'exemplaire du livre restant dans le stock.
        soup : contenue html de la page du livre

	"""
    number_available = extract_attributs_book(soup)['Availability']
    return (number_available.replace("In stock (", "")).replace("available)", "")


def extract_product_description(soup):
    """Extraction de la description du livre.
        soup : contenue html de la page du livre

	"""
    section = soup.find("div", attrs={"id": "content_inner"})
    if section.find("p", attrs=None):
        product_description = (section.find("p", attrs=None).text)
        return product_description
    else:
        return None


def extract_review_rating(soup):
    """Extraction de la note du livre.
        soup : contenue html de la page du livre

	"""
    notes = ("One", "Two", "Three", "Four", "Five" )
    review_rating = "None"
    section = soup.find("div", attrs={"class": "col-sm-6 product_main"})
    for n in notes:
        note = "star-rating " + n
        if section.find("p", attrs={"class": note}):
            review_rating = n     
    return review_rating


def extract_image_url(soup,url):
    """Divise une liste en plusieurs listes.
        l : liste à diviser
        n : taille max des nouvelles listes

	"""
    section = soup.find("div", attrs={"class": "item active"})
    image_url = section.find("img")["src"]
    return url_src_build(url,image_url)


def chunks_liste(l, n):
    """Divise une liste en plusieurs listes.
        l : liste à diviser
        n : taille max des nouvelles listes

	"""
    last = 0
    for i in range(1, n+1):
        cur = int(round(i * (len(l) / n)))
        yield l[last:cur]
        last = cur


def extract_infos_books(url_book):
    """Extraction des info nécessaires pour un livre.
        url_book : url du livre
        	
	"""
    soup = make_soup(url_book)
    i = url_book
    books = {}
    books["product_page_url"] = i
    books["universal_ product_code (upc)"] = extract_upc(soup)
    books["title"] = extract_title(soup)
    books["price_including_taxe"] = extract_price_including_tax(soup)
    books["price_excluding_taxe"] = extract_price_excluding_tax(soup)
    books["number_available"] = extract_number_available(soup)
    books["product_description"] = extract_product_description(soup)
    books["category"] = extract_categorie(soup)
    books["review_rating"] = extract_review_rating(soup)
    books["image_url"] = extract_image_url(soup,i)
    return books 
        

def extract_all_book_of_categorie(categorie, dic_cat):
    """Extraction livres et de leurs info pour une catégorie.
        categorie : categorie des livres
        dic_cat : dictionnaire des catégories (catégorie et son url)
	
	"""
    liste_url_books = list_url_book_categorie(categorie,dic_cat)
    nombre_books = len(liste_url_books)
    nombre_max_url = 100
    taille_sous_liste = math.ceil(nombre_books / nombre_max_url)
    liste_url_books_divise = list(chunks_liste(liste_url_books, taille_sous_liste))
    liste_books = []
    processes = []
    for liste in liste_url_books_divise:
        with ThreadPoolExecutor(max_workers=100) as executor:
            for dic in liste:
                result = processes.append(executor.submit(extract_infos_books, dic))       
    for task in as_completed(processes):
        liste_books.append(task.result())
    return liste_books


def export_to_csv(books,categorie):
    """Export des informations des livres d'une catégorie vers un fichier csv.
        categorie : categorie des livres
        books : liste des dictionnaires de chaque livre
	
	"""
    output = (f"{categorie.replace(' ', '_')}.csv")
    with open( output, "w", encoding="utf-8") as csvfile:
        writer = csv.DictWriter(csvfile, delimiter=',', fieldnames=books[0].keys())
        writer.writeheader()
        for i in books:
            writer.writerows(books)


def download_all_pictures(categorie,books):
    """Téléchargement des images correspondant aux livres d'une catégorie.
        categorie : catégorie des livres
        books : liste des dictionnaires de chaque livre
	
	"""
    directory = "images"
    mkdir_directory(directory)
    liste_books = []
    key_extract = ["universal_ product_code (upc)", "image_url"]
    for book in books:
        liste_books.append({key: book[key] for key in book.keys() & key_extract })
    book_url = []
    book_fullfilename = []
    for book in liste_books:
        name_picture = (f"picture_{categorie.replace(' ', '_')}_upc-{book['universal_ product_code (upc)']}.jpg")
        fullfilename = os.path.join(directory, str(name_picture))
        book_url.append(book["image_url"])
        book_fullfilename.append(str(fullfilename))
    threads = []
    for url,fullfilename in zip(book_url, book_fullfilename):
        thread = threading.Thread(target=download_picture_url, args=(url,fullfilename))
        threads.append(thread)
        thread.start()
    for i in threads:
        i.join()



def download_picture_url(url,fullfilename):
    """Téléchargement d'un fichier.
        url : url du fichier
        fullfilename : chemin avec le nom du fichier cible
	
	"""
    try:
        urllib.request.urlretrieve(url,fullfilename)
    except:
        print (f"Problème lors du téléchargement du fichier {fullfilename} ! \nConnexion impossible à l'url : \
        {url} \n Vérifier votre connexion et relancer le traitement.")
        exit()


def main(url,categorie):
    """Lancement du script.
	
	"""
    try:
        requests.get(url)
    except requests.exceptions.ConnectionError:
        print (f"Connexion impossible à l'url : {url} \nVérifier votre connexion internet.")
        exit()
    start_time = time.time()
    directory_root = (f"extract_{time.strftime('%y%m%d%H%M%S')}")
    mkdir_directory(directory_root)
    dic_cat = dic_categories_url(url)
    os.chdir(directory_root)
    if categorie == "ALL":
        liste_cat = list(dic_cat.keys())
        liste_cat.remove("Books")
        nbre_cat = len(liste_cat)
        compteur = 0
        print(f"Nombre de catégorie à traiter : {nbre_cat}")
        for cat in liste_cat:
            compteur += 1
            print(f"Extraction en cours ... {compteur:2} sur {nbre_cat} ... Catégorie : {cat}")
            dir = cat.replace(" ", "_")
            mkdir_directory(dir)
            os.chdir(dir)
            books = extract_all_book_of_categorie(cat,dic_cat)
            export_to_csv(books,cat)
            download_all_pictures(cat,books)
            os.chdir("../")
    else:
        print(f"Extraction en cours ... Catégorie : {categorie}")
        dir = categorie.replace(" ", "_")
        mkdir_directory(dir)
        os.chdir(dir)
        books = extract_all_book_of_categorie(categorie,dic_cat)
        export_to_csv(books,categorie)
        download_all_pictures(categorie,books)
    print(f"Extraction terminée. \nLe dossier '{directory_root}' contient les fichiers de l'extraction.")
    print(f"Durée du traitement : --- {time.time() - start_time} seconds ---")


# Running the script


URL = "http://books.toscrape.com/"

if __name__ == "__main__":
    main(URL, "ALL")