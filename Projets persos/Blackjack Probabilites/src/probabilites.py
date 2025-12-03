import time, timeit
import matplotlib.pyplot as plt
import random 
import math
import numpy as np
# === Fichier de Gestion des probabilités du Projet ===
verbose = True
perfcount = True

def inVerbose(liste_message):
    if verbose:
        for message in liste_message:
            print("[PROBAS] ", message)
def perf_counter(t1,t0,nom):
    if perfcount:
        print("[PROBAS]", f"⏱ temps {nom} : {t1 - t0:.6f} secondes")
        
## === Fonctions indépendantes ===
### === Fonction de création d'un univers probabiliste sur un jeu de carte de blackjack : toute combinaison en somme cumulée de cartes jusqu"à que la somme soit supérieure à 16 ===
def univers(): #0.60 secondes en moyenne
    t0 = time.perf_counter()
        #### === On initialise la boucle avec une valeur fictive [11] ===
    element = [11]
        #### === On créée la liste de l'univers en question ===
    liste = []
            ##### === Tant que la combinaison n'est pas égale à [1.2.3.4.5.6.7.8.9.10.11.12.13.14.15.16.17.18] on continue de créer des éléments ===
    while (element) != [i for i in range(1,18)]:
        element = prochain(element)
        liste.append(element)
    perf_counter(time.perf_counter(), t0,"calcul de l'univers")
    return liste
### === Fonction nécessaire dans univers() ===
def prochain(element):
    element = element[:]
    element[-1] -= 1
    dernier = element[-1]
    if len(element) >1:
        avantdernier = element[-2]
        if dernier ==avantdernier:
                return prochain(element[:-2] + [dernier])
        if dernier <17:
            while dernier < 17:
                dernier +=10
                element.append(dernier)
            return element
        else: 
            return element
    else:
        if element ==[0]:
            return 
        while dernier < 17:
            dernier +=10
            element.append(dernier)
        return element
    
### === Fonction qui sert juste à convertir une suite mode somme cumulée en suite de cartes exploitables ===      

def somcum_en_cartes(cumsum: list): # 0.34 secondes pour somcum en cartes l'univers entier (peu couteux)
    t0 = time.perf_counter()
    cards =[]
    s=0
    for v in cumsum:
        v = v-s
        s +=v
        cards.append(v)
    #perf_counter(time.perf_counter(), t0, "itératif pour passer de s.cumulées à cartes")
    return cards

"""liste_combin = []
for i in range(1,17):
    combin = []
    for j in range(i):
        if not(combin):
            low = 1
            high = 10
        else:
            low = combin[-1] +1
            high = low +9
        randomn = random.randint(low,high)
        combin.append(randomn)
    liste_combin.append(combin)"""

### === Fonction qui sert juste à convertir une suite de cartes en suite mode somme cumulée exploitables ===      
def cartes_en_somcum(cards):
    cumsum = []
    s = 0
    for c in cards:
        cumsum.append(c+s)
        s += c
    return cumsum

"""liste_carte = []
for i in range(1,18):
    combin = []
    for j in range(i):
        randomt = random.randint(1,10)
        combin.append(randomt)
    liste_carte.append(combin)"""

### === Fonction qui recalcule un univers en fonction des cartes reçu (soit recalcule les possibilités sachant les nouvelles cartes en main) ===
def univers_apres_cartes(cartes, univers):
    t0 = time.perf_counter()
    univers_apres = []
    for combin in univers:
        if (combin[:len(cartes)] == cartes):
            univers_apres.append(combin)
    perf_counter(time.perf_counter(),t0,"Calcul d'un sous univers selon ses cartes")
    return univers_apres


### === Fonction qui recalcule un univers en fonction de la somme cumulée de la suite (le dernier terme de la suite)
def sous_univers_finit_par(univers, finish_by): #0.40 d'éxécution au max
    t0 = time.perf_counter()
    result = [combin for combin in univers if any(combin[-1] == end for end in finish_by)]
    perf_counter(time.perf_counter(), t0, f"univers qui finit par {finish_by}")
    return result

### === Fonction qui retourne la probabilité de tirer une certaine carte dans le paquet du blackjack ===
def proba_de_tirer_un(score, blackjack):
    if score == 10:
        numerateur = blackjack.deck.cpt_cartes[10] + blackjack.deck.cpt_cartes[11] + blackjack.deck.cpt_cartes[12] + blackjack.deck.cpt_cartes[13]
    else:
        numerateur = blackjack.deck.cpt_cartes[score]
    return 100*numerateur/(blackjack.deck.taille()) 

## === Fonctions dépendantes ===
### === Fonction qui recalcule l'univers de chaque joueur du jeu en fonction de leur main en cours, à l'aide de la fonction univers_apres_cartes() ===
def update_univers(de_qui):
    if not(type(de_qui)== list):
        de_qui = [de_qui]
    for joueur in de_qui:
        t0 = time.perf_counter()
        valeurs = []
        for carte in joueur.main.cartes:
            valeurs.append(carte.valeur)
        joueur.univers =  univers_apres_cartes(cartes_en_somcum(valeurs),univers_actif)
        perf_counter(time.perf_counter(), t0, f"pour update l'univers de {joueur}")
        
### === Fonction qui calcule la probabilité de tirer d'obtenir une des suites de cartes d'un ensemble donnée, dans le paquet actif du blackjack ===
def proba_ensemble(ensemble,carteASupprimer, blackjack): #calcule la proba totale de la réalisation d'une des combinaisons
    t0 = time.perf_counter()
    proba = 0.
    for combin in ensemble: #pour chaque combinaison dans l'ensemble des combinaisons choisi
        deck_len = blackjack.deck.taille() #longueur du paquet choisi moins la stopcard
        proba_combin = 1.
        
        cartes = somcum_en_cartes(combin)[carteASupprimer::] #on récupère la combinaison moins les cartes déja sortis
        for carte in list(set(cartes)): #pour chaque exemplaire unique de chaque carte dans la combinaison
            nb_copy_cartes = cartes.count(carte) #on compte le nombre de copie présente de cette carte dans la combin
            if carte == 10:
                nb = blackjack.deck.cpt_cartes[10] + blackjack.deck.cpt_cartes[11] + blackjack.deck.cpt_cartes[12]+blackjack.deck.cpt_cartes[13]
            else:
                nb = blackjack.deck.cpt_cartes[carte] #on vient chercher le nombre de copie de cette carte dans le deck
            for i in range(nb_copy_cartes): #pour chaque exemplaire de la carte en cours (nb de copie de la carte)
                numer = max(nb-i, 0) #on s'assure que le nombre de copie dans le deck est suffisant (sinon 0)
                proba_combin *= ((numer/deck_len)) #formule de proba 
                deck_len -=1 #on simule le retrait de la carte sortie
        proba += proba_combin
    perf_counter(time.perf_counter(), t0, f"pour calculer la proba de l'ensemble des possibilités de {len(ensemble)} combinaisons")
    return proba

"""univ = univers()
univers_croupier = univers_apres_cartes([1], univ)
bust = sous_univers_finit_par(univers_croupier, [22,23,24,25,26])
proba = proba_ensemble_bis(bust,1)
print(proba)"""

### === Fonction qui renvoie un sous ensemble des suites de cartes qui font bust le joueur en fonction de ses mains en cours ===
def sous_ensemble_du_bust(joueur):
    total = sous_univers_finit_par(joueur.univers,[22,23,24,25,26])
    return total
### === Fonction finale qui renvoie la probabilité de bust  pour tous les joueurs choisis en entrée, dans le jeu de blackjack choisi ===
def proba_bust(sur_qui :list,blackjack):
    if not(type(sur_qui) == list):
        sur_qui = [sur_qui]
    #### === On update les univers avant de calculer la probabilité
    update_univers(sur_qui)
    #### === Pour tous les joueurs de la liste, on génère le sous ensemble des mains qui nous font bust, et on calcule la proba de tomber sur une de ces mains ===
    for joueur in sur_qui:
        bust = sous_ensemble_du_bust(joueur)
        proba = round(100*proba_ensemble(bust,len(joueur.main.cartes),blackjack),2)
        joueur.main.proba_bust = proba # on l'inscrit bien dans la classe du joueur

univers_actif = univers()

def proba_score(quel_score, sur_qui, blackjack):
    if not(type(quel_score) == list):
        quel_score = [quel_score]
    #### === On update les univers avant de calculer la probabilité
    update_univers(sur_qui)
    #### === on génère le sous ensemble des mains qui nous finissent par 17, et on calcule la proba de tomber sur une de ces mains ===
    univers_score = sous_univers_finit_par(sur_qui.univers,quel_score)
    proba = round(100*proba_ensemble(univers_score,len(sur_qui.main.cartes),blackjack),2)
    return proba
    
    