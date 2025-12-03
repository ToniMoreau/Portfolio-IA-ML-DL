import numpy as np
import time

PERF_COUNTER = False
VERBOSE = False
def perf_counter(t1,t0, nom):
    if PERF_COUNTER:
        print(f"⏱ temps {nom} : {t1 - t0:.6f} seconds")
        print("-"*30)
def inVerbose(texte_liste):
    if VERBOSE:
        print("-"*30)
        for texte in texte_liste:
            print("➡ ",texte)
    
class Carte:
    def __init__(self):
        nom = "None"
        pass 
    def __str__(self):
        return "Carte"
    
    def défausser(self,fausse):
        pass
        
class CarteDeJeu(Carte): 
    couleurs = ("coeur", "carreau", "trèfle", "pique") 
    valeurs = {1 : ["As", 1, "01"], 11: ["Valet", 10,"V"], 12:["Dame", 10, "D"], 13:["Roi", 10, "R"]} 
    def __init__(self ,numero, couleur=None): 
        super().__init__()
        self.numero = numero 
        self.nom = self.valeurs[numero][0] if numero in list(self.valeurs.keys()) else str(numero) 
        self.couleur = couleur
        if self.nom == "As":
            self.image = f"cartes/01-{self.couleur}.jpg"
        else:
            self.image = f"cartes/{"0" if self.nom.isdigit() and self.nom != "10" else""}{self.nom if self.nom.isdigit() else self.nom[0]}-{self.couleur}.jpg"
        
        
    def __str__(self): 
        return f"{self.nom} de {self.couleur}" 
    @property 
    def valeur(self): 
            return self.valeurs[self.numero][1] if self.numero in list(self.valeurs.keys()) else self.numero 

    def ajouter_à(self, tas : "TasDeCartes"):
        tas.ajouter(self)

    def défausser(self, fausse):
        super().défausser(fausse)
        self.ajouter_à(fausse)

class StopCard(Carte):
    def __init__(self):
        super().__init__()
        self.nom = "StopCard"
        self.numero = 0
        self.valeur = 0

class TasDeCartes():
    def __init__(self):
        self.cartes :list[Carte] = []
        self.cpt_cartes = {}
        for i in range(0,15):
            self.cpt_cartes[i] = 0
        
    def __str__(self):
        return f"Tas de {len(self.cartes)} cartes." 
    def update_cpt_cartes(self):
        for i in range(0,15):
            self.cpt_cartes[i] = 0
        for carte in self.cartes:
            self.cpt_cartes[carte.numero] +=1
            
    def nb_carte_du_score(self, score):
        cartes_du_score = [p for p in self.cartes if p.valeur == score]
        return len(cartes_du_score)
    
    def taille(self):
        return len(self.cartes)  
    
    def tirer(self):
        return self.cartes.pop()
    
    def ajouter(self, tas : list[Carte], position = None):
        if isinstance(tas, Carte):
            tas = [tas]
        if not(position):
            for carte in tas:
                self.cpt_cartes[carte.numero] +=1
                self.cartes.append(carte)
        else:
            for carte in tas:
                self.cartes.insert(position, carte)
                self.cpt_cartes[carte.numero] +=1
                
                position +=1
        tas.clear()
        

    def inserer_dans(self, receveur: "TasDeCartes", à_insérer: list[Carte] | Carte | None = None):
        # Si on ne précise rien -> transférer toutes les cartes
        if not(à_insérer):
            à_insérer = self.cartes[:]  # copie
            self.cartes.clear()         # on vide le paquet
            # Gestion des cpt cartes
            for keys in self.cpt_cartes.keys():
                self.cpt_cartes[keys] = 0

        elif isinstance(à_insérer, Carte):
            if à_insérer in self.cartes:
                self.cartes.remove(à_insérer)
                self.cpt_cartes[à_insérer.numero] -=1 #update cpt
            à_insérer = [à_insérer]

        else:
            # Si c'est une sous-liste -> on supprime ces cartes du self
            for carte in à_insérer:
                if carte in self.cartes:
                    self.cpt_cartes[carte.numero] -=1 #update cpt
                    self.cartes.remove(carte)
                    
                    

        # Ajouter dans le receveur
        receveur.ajouter(à_insérer)
        return True       
     
class Paquet(TasDeCartes):
    def __init__(self):
        super().__init__()

        for couleur in CarteDeJeu.couleurs:
            for i in range(1,14):
                carte = CarteDeJeu(i, couleur)
                self.ajouter(carte)
    
    def __str__(self):
        return f"Paquet de {len(self.cartes)} cartes." 
    
class Main(TasDeCartes): 
    def __init__(self): 
        super().__init__()
        self.tuple = False
        self.proba_bust = 0
        self.result = ""
        
    def __str__(self): 
        texte = "" 
        for carte in self.cartes: 
            texte += f"{carte}, " 
        
        return texte 
                      
    @property 
    def valeur(self): #validée en opti
        inVerbose([f"Calcul de valeur de {self} begins..."])
        t0 = time.perf_counter()
        val1 = 0 
        un = False
        for carte in self.cartes:
            if not(un):
                un = (carte.valeur ==1)
            val1 += carte.valeur 
        
        val2 = val1 + un*10
            
        t1 = time.perf_counter()
        perf_counter(t1,t0,"déterminer valeur d'une main")

        if val1 == val2 or val2 >21:
            self.tuple = False
            return val1
        if val2 == 21:
            self.tuple = False
            return val2
        self.tuple = True
        return (val1, val2)

    def défausser(self, fausse: TasDeCartes):
        self.inserer_dans(fausse, à_insérer=None)

class Deck(TasDeCartes): 
    def __init__(self): 
        super().__init__()
        self.fausse : TasDeCartes | None = TasDeCartes()
        self.a_shuffle = True 
        self.stop_card = StopCard() 
        
    def taille(self):
        tail = super().taille()
        if self.stop_card in self.cartes:
            inVerbose(['Stop card dans le deck'])
            return tail - 1
        return tail
    def shuffle_stop(self): #robustesse à confirmer, vitesse 3.51251e-05 secondes
        inVerbose(["shuffle_stop begins..."]) 
        t0 = time.perf_counter()
        
        self.ajouter(self.fausse.cartes)
         
        
        np.random.shuffle(self.cartes) #On mélange 

        index1 = int(0.1*len(self.cartes)) 
        index2 = int(0.4*len(self.cartes))
        index = np.random.randint(index1, index2)
        self.ajouter(self.stop_card, index) #on insère la stop card 
        self.cpt_cartes[0] +=1
        
        for carte in self.cartes[:5]:
            self.cartes.remove(carte)
            self.cpt_cartes[carte.numero] -=1
            carte.défausser(self.fausse)
        
        self.a_shuffle = False 
        t1 = time.perf_counter()
        perf_counter(t1,t0,"shuffle_stop")
        return True 
    
    def tirer(self): 
        carte : Carte = super().tirer() #on tire une carte 
        if carte.nom == "StopCard": #Si c'est la stop card: 
            self.a_shuffle = True 
            print("Carte Stop sortie") 
            self.cpt_cartes[carte.numero ] -=1
            carte = self.tirer()
        self.cpt_cartes[carte.numero] -=1
        return carte
        
    def défausser(self):
        self.inserer_dans(self.fausse, à_insérer=None)

       