# DA_Python_P02 - SCRAPE

Utilisez les bases de Python pour l'analyse de marché

# Table of Contents <a name="Table_of_Contents"></a>
- [DA_Python_P02 - SCRAPE](#da_python_p02---scrape)
- [Table of Contents <a name="Table_of_Contents"></a>](#table-of-contents-)
  - [INTRODUCTION <a name="INTRODUCTION"></a>](#introduction-)
  - [Objectifs du projet <a name="objectifs"></a>](#objectifs-du-projet-)
  - [FEATURES <a name="FEATURES"></a>](#features-)
  - [REQUIREMENTS <a name="REQUIREMENTS"></a>](#requirements-)
    - [Récupération du projet <a name="Recup_projet"></a>](#récupération-du-projet-)
    - [Création d'un environnement virtuel Python <a name="Env_Virtuel_Python"></a>](#création-dun-environnement-virtuel-python-)
    - [Installation des packages Python nécessaire <a name="Installation_package"></a>](#installation-des-packages-python-nécessaire-)
  - [Comment utiliser le script "p2_scrape.py" <a name="How_to_use"></a>](#comment-utiliser-le-script-p2_scrapepy-)
  - [Exemple d'affichage de sortie du "p2_scrape.py" <a name="How_to_use"></a>](#exemple-daffichage-de-sortie-du-p2_scrapepy-)
  - [Localisation du dossier d'extraction <a name="Options"></a>](#localisation-du-dossier-dextraction-)
  - [Fichier d'extration "csv" <a name="Csv"></a>](#fichier-dextration-csv-)
  - [Fichier d'extration "image des livres" <a name="Image_livre"></a>](#fichier-dextration-image-des-livres-)
  - [Options <a name="Options"></a>](#options-)
  - [Contact <a name="Contact"></a>](#contact-)



## INTRODUCTION <a name="INTRODUCTION"></a>

p2_scrape.py est script Python qui automatise l'extraction des informations sur les livres vendues
sur le site "http://books.toscrape.com/" .


## Objectifs du projet <a name="objectifs"></a>

L'objectif est de suivre les prix des livres chez Books to Scrape, un revendeur de livres en ligne. 
En pratique le programme n'effectuera pas une véritable surveillance en temps réel des prix sur la durée. 
Il s'agira simplement d'une application exécutable à la demande visant à récupérer les prix au moment de son exécution.


[<div align="center">[Table of Contents]</div>](#Table_of_Contents) 

## FEATURES <a name="FEATURES"></a>

  - Récupère toutes les catégories de livre du site.
  - Extrait vers un fichier "csv" les attributs importants de chaque livre et pour toutes les catégories.
  - Télécharge les images de chaque livre.
  - Création d'un dossier parent qui contiendra des sous dossiers pour chaque catégorie.


[<div align="center">[Table of Contents]</div>](#Table_of_Contents)

## REQUIREMENTS <a name="REQUIREMENTS"></a>
  - Pour l'exécution du programme, une version de Python d'au moins v3.8.X ou plus récente est recommandée.
  - Il est recommandé d'utiliser un environnement virtuel Python et d'installer les packages présents dans le fichier "requirements.txt" (une procédure plus bas vous détaillera cette installation).
  - Il est recommander de récupérer le projet en utilisant "git clone" ou en téléchargeant directement le projet.
  - Une connexion internet fonctionnelle est nécessaire


### Récupération du projet <a name="Recup_projet"></a>

- Par téléchargement:
  
 lien de téléchargement : https://github.com/lahou-sys/DA_Python_P02/archive/refs/heads/main.zip

- Par "git clone":
  
```ssh
git clone https://github.com/lahou-sys/DA_Python_P02.git
```


[<div align="center">[Table of Contents]</div>](#Table_of_Contents) 

### Création d'un environnement virtuel Python <a name="Env_Virtuel_Python"></a>

Se positionner dans le dossier de votre choix et qui hébergera le script "p2_scrape.py".

Si le module python "venv" n'est pas installé sur votre système, il est nécessaire de l'installer comme ci-dessous :

  - Installation du module "venv"

```ssh
$ pip install venv
```

  - Création de l'environnement virtuel Python

```ssh
$ python3 -m venv .venv
```

  - Activation de l'environnement virtuel Python

```ssh
$ source ./.venv/bin/activate
```

[<div align="center">[Table of Contents]</div>](#Table_of_Contents) 

### Installation des packages Python nécessaire <a name="Installation_package"></a>

l'installation de ces packages sont nécessaire pour la bonne éxécution du script.

- bs4==0.0.1
- requests==2.26.0

    - Installation automatique des packages

```ssh
$ pip install -r requirements.txt
```


[<div align="center">[Table of Contents]</div>](#Table_of_Contents) 


## Comment utiliser le script "p2_scrape.py" <a name="How_to_use"></a>

Une fois l'environnement virtuel Python créé et activé, ainsi que l'installation des packages nécessaires installés.

Vous pouvez lancer le programme "p2_scrape.py" :

```ssh
$ python3 ./p2_scrape.py
```

[<div align="center">[Table of Contents]</div>](#Table_of_Contents) 

## Exemple d'affichage de sortie du "p2_scrape.py" <a name="How_to_use"></a>

```ssh
Nombre de catégorie à traiter : 50
Extraction en cours ...  1 sur 50 ... Catégorie : Travel
Extraction en cours ...  2 sur 50 ... Catégorie : Mystery
Extraction en cours ...  3 sur 50 ... Catégorie : Historical Fiction
Extraction en cours ...  4 sur 50 ... Catégorie : Sequential Art
Extraction en cours ...  5 sur 50 ... Catégorie : Classics
Extraction en cours ...  6 sur 50 ... Catégorie : Philosophy
Extraction en cours ...  7 sur 50 ... Catégorie : Romance
Extraction en cours ...  8 sur 50 ... Catégorie : Womens Fiction
Extraction en cours ...  9 sur 50 ... Catégorie : Fiction
Extraction en cours ... 10 sur 50 ... Catégorie : Childrens
Extraction en cours ... 11 sur 50 ... Catégorie : Religion
Extraction en cours ... 12 sur 50 ... Catégorie : Nonfiction
Extraction en cours ... 13 sur 50 ... Catégorie : Music
Extraction en cours ... 14 sur 50 ... Catégorie : Default
Extraction en cours ... 15 sur 50 ... Catégorie : Science Fiction
Extraction en cours ... 16 sur 50 ... Catégorie : Sports and Games
Extraction en cours ... 17 sur 50 ... Catégorie : Add a comment
Extraction en cours ... 18 sur 50 ... Catégorie : Fantasy
Extraction en cours ... 19 sur 50 ... Catégorie : New Adult
Extraction en cours ... 20 sur 50 ... Catégorie : Young Adult
Extraction en cours ... 21 sur 50 ... Catégorie : Science
Extraction en cours ... 22 sur 50 ... Catégorie : Poetry
Extraction en cours ... 23 sur 50 ... Catégorie : Paranormal
Extraction en cours ... 24 sur 50 ... Catégorie : Art
Extraction en cours ... 25 sur 50 ... Catégorie : Psychology
Extraction en cours ... 26 sur 50 ... Catégorie : Autobiography
Extraction en cours ... 27 sur 50 ... Catégorie : Parenting
Extraction en cours ... 28 sur 50 ... Catégorie : Adult Fiction
Extraction en cours ... 29 sur 50 ... Catégorie : Humor
Extraction en cours ... 30 sur 50 ... Catégorie : Horror
Extraction en cours ... 31 sur 50 ... Catégorie : History
Extraction en cours ... 32 sur 50 ... Catégorie : Food and Drink
Extraction en cours ... 33 sur 50 ... Catégorie : Christian Fiction
Extraction en cours ... 34 sur 50 ... Catégorie : Business
Extraction en cours ... 35 sur 50 ... Catégorie : Biography
Extraction en cours ... 36 sur 50 ... Catégorie : Thriller
Extraction en cours ... 37 sur 50 ... Catégorie : Contemporary
Extraction en cours ... 38 sur 50 ... Catégorie : Spirituality
Extraction en cours ... 39 sur 50 ... Catégorie : Academic
Extraction en cours ... 40 sur 50 ... Catégorie : Self Help
Extraction en cours ... 41 sur 50 ... Catégorie : Historical
Extraction en cours ... 42 sur 50 ... Catégorie : Christian
Extraction en cours ... 43 sur 50 ... Catégorie : Suspense
Extraction en cours ... 44 sur 50 ... Catégorie : Short Stories
Extraction en cours ... 45 sur 50 ... Catégorie : Novels
Extraction en cours ... 46 sur 50 ... Catégorie : Health
Extraction en cours ... 47 sur 50 ... Catégorie : Politics
Extraction en cours ... 48 sur 50 ... Catégorie : Cultural
Extraction en cours ... 49 sur 50 ... Catégorie : Erotica
Extraction en cours ... 50 sur 50 ... Catégorie : Crime
Extraction terminée. 
Le dossier 'extract_210915215826' contient les fichiers de l'extraction.
Durée du traitement : --- 161.05823349952698 seconds ---
```

[<div align="center">[Table of Contents]</div>](#Table_of_Contents)

## Localisation du dossier d'extraction <a name="Options"></a>

Le script "p2_scrape.py" crééra un nouveau dossier parent horodaté lors de chaque éxécution, il se nommera comme ci-dessous :

extract_YYMMJJHHmmss

- YY : année
- MM : mois
- JJ : jour
- HH : heure
- mm : minute
- ss : second

Exemple :

```ssh
extract_210915213844
```

Ce dossier parent contiendra des sous dossier pour chaque catégorie.

Exemple d'un sous dossier de la catégorie "Art":

```ssh
├── Art
│   ├── Art.csv
│   └── images
│       ├── picture_Art_upc-3eec766dda26fa64.jpg
│       ├── picture_Art_upc-4b8fa561a1e52d1c.jpg
│       ├── picture_Art_upc-66a4e422b212726a.jpg
│       ├── picture_Art_upc-8a150fd8ff5d7686.jpg
│       ├── picture_Art_upc-9147c5251cc99eb1.jpg
│       ├── picture_Art_upc-9194ae88379dbf1a.jpg
│       ├── picture_Art_upc-ccd9ffa25efabdea.jpg
│       └── picture_Art_upc-d6d9ffea95f2f8bf.jpg

```

Dans ce sous dossier, nous retrouvons le fichiers CSV qui contient toutes les informations concernant les livres de cette catégorie et un sous dossier "images" qui contient toutes les images des livres de cette catégorie.


[<div align="center">[Table of Contents]</div>](#Table_of_Contents)


## Fichier d'extration "csv" <a name="Csv"></a>

Lors de l'extraction, plusieurs informations concernant les livres d'une catégorie sont enregistrés dans un fichier "csv" et par catégorie.

Les champs suivants sont récupérés :

- product_page_url
- universal_ product_code (upc)
- title
- price_including_tax
- price_excluding_tax
- number_available
- product_description
- category
- review_rating
- image_url


[<div align="center">[Table of Contents]</div>](#Table_of_Contents)


## Fichier d'extration "image des livres" <a name="Image_livre"></a>

Les images de chaque livre sont téléchargées et rangées par catégorie.

Les fichiers images sont nommé de cette façon :


picture_[catégorie]_upc-[numéro UPC].jpg


Par exemple :

```ssh
picture_Art_upc-3eec766dda26fa64.jpg
```

[<div align="center">[Table of Contents]</div>](#Table_of_Contents)



## Options <a name="Options"></a>

Si vous souhaitez lancer l'extraction uniquement sur une catégorie de livre, vous avez la possibilité de le faire en éditant le script "p2_scrape.py" et en modifiant le code comme ci-dessous:

La ligne 402 appelle la fonction "main"

- Avant

```python
URL = "http://books.toscrape.com/"

if __name__ == "__main__":
    main(URL, "ALL")
```

- Après

A la place de "ALL", vous pouvez rentrer la catégorie voulue, dans notre exemple "Travel". attention c'est sensibble à la casse.

```python
URL = "http://books.toscrape.com/"

if __name__ == "__main__":
    main(URL, "Travel")
```

[<div align="center">[Table of Contents]</div>](#Table_of_Contents)

## Contact <a name="Contact"></a>

Mail : lbenmoulay@gmail.com