
from classes import *
import probabilites
from optimisation.vitesse import *
from optimisation.robustesse import *
import timeit

perfcount = True
def perf_counter(t1,t0, nom):
    if perfcount:
        print(f"[TEST OPTI] ⏱ temps {nom} : {t1 - t0:.6f} seconds")
        print("-"*30)


paquet1 = Paquet()
paquet2 = Paquet()
paquet3 = Paquet()
paquet4 = Paquet()
    ## === Création du deck et ajout des paquets dans le deck
deck = Deck()
deck.ajouter(paquet1.cartes)
deck.ajouter(paquet2.cartes)
deck.ajouter(paquet3.cartes)
deck.ajouter(paquet4.cartes)

univ = probabilites.univers_apres_cartes([3], probabilites.univers())
bust = probabilites.sous_univers_finit_par(univ, [22,23,24,25,26])
t_total = time.perf_counter()

for combin in bust:
    cartes = probabilites.somcum_en_cartes(combin)[1::]
    for carte in list(set(cartes)):
        nb = deck.nb_carte_du_score(carte)
        
perf_counter(time.perf_counter(), t_total,f"pour nb carte score en boucle :{len(univ)}")