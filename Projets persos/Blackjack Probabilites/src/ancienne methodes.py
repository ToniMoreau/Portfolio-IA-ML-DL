def valeur(self): 
    """val1 = 0 
    val2 = 0
    un = False
    for carte in self.cartes:
        un = 10* (carte.valeur ==1)
        val1 += carte.valeur 
    
    val2 = val1 + un
        

    if val1 == val2:
        return val1

    if val2 < 17:
        self.tuple = True
        return (val1,val2)
    self.tuple = False
    if val2 < 22:
        return val2
    else: return min(val1, val2)  """

def valeurs(self, i =0):
    """if i == len(self.cartes)-1:
        return [self.cartes[i].valeur]
    
    else: 
        return [self.cartes[i].valeur] + self.valeurs(i+1)"""

"""def shuffle_stop1(self):
    inVerbose(["shuffle_stop begins..."]) 
    t0 = time.perf_counter()
    
    fausse_copy = self.fausse.cartes[:]
    self.ajouter(fausse_copy)
    self.fausse.cartes.clear()
    
    
    np.random.shuffle(self.cartes) #On mélange 

    index1 = int(0.1*len(self.cartes)) 
    index2 = int(0.4*len(self.cartes))
    index = np.random.randint(index1, index2)
    self.ajouter(self.stop_card, index) #on insère la stop card 
    
    for carte in self.cartes[:5]:
        self.cartes.remove(carte)
        carte.défausser(self.fausse)
    
    self.a_shuffle = False 
    t1 = time.perf_counter()
    perf_counter(t1,t0,"shuffle_stop")
    return True 
"""

"""def somcum_en_cartes_rec(cumsum: list):
    
    if not(cumsum):
        return []
    if len(cumsum) <=1:
        return cumsum
    else:
        return somcum_en_cartes_rec(cumsum[:-1]) + [cumsum[-1] - cumsum[-2]]"""
        
"""y_iter = []
x = []
y_rec = []
for combin in liste_combin:
    lencomb = len(combin) 
    combinrec = combin[:]
    
    t_iter= time.perf_counter()
    somcum_en_cartes(cumsum=combin)
    t_iter = time.perf_counter() - t_iter
    
    y_iter.append(t_iter)
    
    t_rec = time.perf_counter()
    somcum_en_cartes_bis(cumsum=combinrec)
    t_rec = time.perf_counter() - t_rec
    
    y_rec.append(t_rec)
    
    x.append(lencomb)

plt.plot(x,(y_rec),'r')
plt.plot(x, (y_iter),'b')
plt.xlabel("nombre de carte dans la main")
plt.ylabel("temps (secondes)")
plt.legend(["récursif", "itératif"])
plt.show()"""

"""def proba_ensemble_original(ensemble,carteASupprimer, blackjack): #calcule la proba totale de la réalisation d'une des combinaisons
    t0 = time.perf_counter()
    proba = 0.
    for combin in ensemble: #pour chaque combinaison dans l'ensemble des combinaisons choisi
        deck_len = blackjack.deck.taille() #longueur du paquet choisi moins la stopcard
        proba_combin = 1.
        
        cartes = somcum_en_cartes(combin)[carteASupprimer::] #on récupère la combinaison moins les cartes déja sortis
        for carte in list(set(cartes)): #pour chaque exemplaire unique de chaque carte dans la combinaison
            nb_copy_cartes = cartes.count(carte) #on compte le nombre de copie présente de cette carte dans la combin
            nb = blackjack.deck.nb_carte_du_score(carte) #on vient chercher le nombre de copie de cette carte dans le deck
            for i in range(nb_copy_cartes): #pour chaque exemplaire de la carte en cours (nb de copie de la carte)
                numer = max(nb-i, 0) #on s'assure que le nombre de copie dans le deck est suffisant (sinon 0)
                proba_combin *= ((numer/deck_len)) #formule de proba 
                deck_len -=1 #on simule le retrait de la carte sortie
        proba += proba_combin
    perf_counter(time.perf_counter(), t0, f"pour calculer la proba de l'ensemble des possibilités de {len(ensemble)} combinaisons")
    return proba
"""