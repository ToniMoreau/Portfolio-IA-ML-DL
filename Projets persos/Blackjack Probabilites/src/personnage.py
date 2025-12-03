from classes import *

# === Classe Mère des joueurs et croupiers, inutilisable ===
class Entité:
    def __init__(self, ID, nom, compte = None):
        self.ID = ID
        self.nom = nom
        self._main : Main = Main()
        self.univers = []
        self.mise = 2
        self.compte = compte
    def __str__(self):
        return self.nom    
    @property 
    def main(self): 
        return self._main 
## === Sous classe des joueurs ===
class Joueur(Entité): 
    def __init__(self, ID, nom, compte = None): 
        super().__init__(ID, nom, compte)
        self.est_couché = False 
        self.choix = None # dernier choix en cours (se coucher/tirer)
         
    def __str__(self):
        return self.nom     
    def décision(self): 
        #sleep(1)
        print(self.main.tuple)
        print(self.main.valeur)
        if self.main.tuple:
            valeur = max(self.main.valeur)
        else : valeur = self.main.valeur
        if valeur <= 16: 
            return "hit" 
        else: return "sleep" 
## === Sous classes de croupiers ===
class Croupier(Entité): 
    def __init__(self,ID, nom, compte = None): 
        super().__init__(ID, nom, compte) 
        self.est_couché = False
        self.choix = None # dernier choix en cours (se coucher/tirer)
        
    def __str__(self):
        return self.nom  
    def décision(self): 
        #sleep(1)
        if self.main.tuple:
            valeur = max(self.main.valeur)
        else : valeur = self.main.valeur
        if valeur <= 16: 
            return "hit" 
        else: return "sleep"
