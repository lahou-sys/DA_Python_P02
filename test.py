""" def message(m):
    m = str(m)
    v = input(m)
    t = type(v)
    r = t is int
    #print(r)
    while r is False:
        print(r)
        v = input(m)
    if r is True:
        print(r)
        return v
    else:
        print(r)
        v = input(m)
   

def tableMult():
    x = message("Rentrer le chiffre multiplicateur : ")
    y = message("Rentrer la plage de multiplication : ")
    table = str(x)
    print("Table de multiplication :  {}".format(x))
    for i in range(y+1):
        r = i*x
        print("{} X {} = {}".format(i,x,r))

tableMult() """

stoplist = []

stoplist = 'ce de du en le la mais on ou au aux par pas pour qui un une et ne à là je tu il elle vous nous ils elles que sa son'.split()


ponctuation = "!()-[]{};:\'\"`,< >./?@#$%^&*~"

mot_liste = ['la', 'cigale,', 'ayant', 'chanté', 'tout', "l'été,", 'se', 'trouva', 'fort', 'dépourvue', 'quand', 'la', 'bise', 'fut', 'venue.', 'pas', 'un', 'seul', 'petit', 'morceau', 'de', 'mouche', 'ou', 'de', 'vermisseau.', 'elle', 'alla', 'crier', 'famine', 'chez', 'la', 'fourmi', 'sa', 'voisine,', 'la', 'priant', 'de', 'lui', 'prêter', 'quelque', 'grain', 'pour', 'subsister', "jusqu'à", 'la', 'saison', 'nouvelle.', 'je', 'vous', 'paierai,', 'lui', 'dit-elle,', 'avant', "l'oût,", 'foi', "d'animal,", 'intérêt', 'et', 'principal.', 'la', 'fourmi', "n'est", 'pas', 'prêteuse', ';', "c'est", 'là', 'son', 'moindre', 'défaut.', 'que', 'faisiez-vous', 'au', 'temps', 'chaud', '?', 'dit-elle', 'à', 'cette', 'emprunteuse.', 'nuit', 'et', 'jour', 'à', 'tout', 'venant', 'je', 'chantais,', 'ne', 'vous', 'déplaise.', 'vous', 'chantiez', '?', "j'en", 'suis', 'fort', 'aise.', 'eh', 'bien', '!dansez', 'maintenant.'] 


def pilote(fichier, idx):
    with open(fichier, 'r', encoding='utf8') as fp:
        # on itere sur le fichier ligne par ligne
        for i, ligne in enumerate(fp):
            indexe(idx, ligne.split(), i)

def ajoute(idx, mot, ligne):
    # si le mot ne se trouve pas encore dans l'index, 
    # initialise les occurences par une liste vide
    if mot not in idx:
        idx[mot] = []
    # si la ligne n'a pas encore ete enregistree pour ce mot
    if ligne not in idx[mot]:
        # on ajoute le numero de ligne correspondant au mot
        idx[mot].append(ligne)

def indexe(idx,liste):
    # on itere sur les mots
    for mot in idx:
        # met obligatoirement en minuscule
        mot = mot.lower()
        # nettoyage du mot, voir ci-apres
        mot = nettoie(mot)
        # on en profite pour verifier si on veut 
        # vraiment indexer ce mot
        if mot and mot not in stoplist:
            liste.append(mot)
    return liste
            

def nettoie(mot):
    if mot[-1] in ponctuation:
        mot=mot[:-1]
        if ((len(mot) > 2) and (mot[1] in ponctuation)):
            mot=mot[2:]
    elif mot[0] in ponctuation:
        mot=mot[1:]
    elif ((len(mot) > 2) and (mot[1] in ponctuation)):
        mot=mot[2:]
    elif mot.lower() in stoplist:
        pass
    return mot

def prd(idx):
    for mot in sorted(idx):
        print('\t', mot, ':', idx[mot])

index = {}


new_liste = []

for m in mot_liste:
    new_liste.append(nettoie(m))

print(stoplist)
print("")
print(new_liste)
print(len(new_liste))
print("")

print(ponctuation)
print(mot_liste)
print("")
new_liste = []
print(indexe(mot_liste,new_liste))
print(len(indexe(mot_liste,new_liste)))