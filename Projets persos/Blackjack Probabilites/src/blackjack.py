from classes import * 
from personnage import *
from banque import Compte

# === La classe qui s'occupe de toutes les étapes du jeu blackjack ===    
class BlackJack:
## === Initialisation ===
    def __init__(self, croupier: Croupier, joueurs : list[Joueur], deck: Deck | None = None, nb_paquets = 4 , tapis = Entité(4,"Tapis")):
        self.verbose = True #Pour débugger
        self.perfcount = True
        self.tapis = tapis
        self.tapis.compte = Compte(0,self.tapis)
    ### === Initialisation du blackjack, on récupère toutes les variables d'entrée et on créée les autres nécessaire ===
        self.nombre_paquets_dans_deck = nb_paquets #on récupère le nombre de paquets du deck
        self.deck = deck
        deck.update_cpt_cartes()
        self.deck.shuffle_stop() # on mélange le deck à l'initialisation
        self.croupier = croupier  # on initialise le croupier choisi
        self.joueurs : Joueur = joueurs #liste des joueurs présent pour le blackjack
 
    @property 
    def liste_joueur_debout(self): 
        liste = [] 
        for joueur in self.joueurs: 
            if not(joueur.est_couché): 
                liste.append(joueur) 
        return liste 
    
    def inVerbose(self, liste_vocaux):
        if self.verbose:
            for element in liste_vocaux:
                print("[JEU]",element)
    def perf_counter(self, t1,t0, nom):
        if self.perfcount:
            print("[JEU]",f"⏱ temps {nom} : {t1 - t0:.6f} secondes")
            print("-"*30)
            
        
## === Fonctions principale de déroulement ===
    ### Lancement de la partie (2 cartes par joueur, une au croupier)
    def lancer_partie(self): 
        self.inVerbose(["-"*50,"Lancement de la partie","-"*50])
            #### === On réveille tous les joueurs ===
        for joueur in self.joueurs + [self.croupier]:
            joueur.est_couché = False
            #### === On mélange si nécessaire
        for joueur in self.joueurs:
            joueur.compte.virement(joueur.mise, self.tapis)
        if self.deck.a_shuffle: 
            self.deck.shuffle_stop() #si la carte stop est passée on mélange
            
        self.inVerbose([f"{"-"*50} DISTRIBUTION DES 2 CARTES A CHACUN  {"-"*50}"])
            #### === Distribution des cartes ===
                ##### === Premier tour de table joueurs ===
        t_lancement = time.perf_counter()

        self.tour_de_table() 
                ##### === Distribution de la carte du croupier ===
        self.distribuer_carte(self.croupier)
                ##### === Deuxième tour de table joueurs ===
        self.tour_de_table()
        self.perf_counter(time.perf_counter(), t_lancement, "premier tour distribution des cartes")
        
        for joueur in self.liste_joueur_debout + [self.croupier]: 
            self.inVerbose([f"{joueur}  : {joueur.main}"])
    
    ### === Phase 2, les joueurs tirent ou se couchent ===
    def tirer_ou_se_coucher(self, joueur :Joueur, decision): 
            #### === Le joueur tire une nouvelle carte ===
        t_tour2 = time.perf_counter()
        if decision == "hit": 
            self.distribuer_carte(joueur) #distribution de la carte
            self.inVerbose([f"{joueur} tire un {joueur.main.cartes[-1]}", f"nouvelle valeur : {joueur.main.valeur}"])
                ##### === Gestion du couché après distribution ===
                    ###### === Si le joueur à blackjack ou + on se couche automatiquement ===
            joueur_valeur = joueur.main.valeur 
            if type(joueur_valeur) == int and joueur_valeur >= 21:
                self.inVerbose([f"le joueur {joueur} se couche avec {joueur_valeur}"]) 
                joueur.est_couché = True
            #### === Le joueur se couche ===
        elif decision == "sleep": 
            joueur.est_couché = True 
            self.inVerbose([f"le joueur {joueur} se couche avec {joueur.main.valeur}"]) 
        else:
            pass
        self.perf_counter(time.perf_counter(), t_tour2, "tour décisions")
        return True
    ### === Phase 3, le croupier tire toutes ses cartes ===
    def décision_croupier(self):
        self.inVerbose([f"{"-"*50}  DECISION DU CROUPIER {"-"*50}"])
        t_croupier_décide = time.perf_counter()
        #### === Tant que le croupier n'est pas couché il tire une carte ===
        while not(self.croupier.est_couché):
            self.tirer_ou_se_coucher(self.croupier, self.croupier.décision())
            self.inVerbose([f"{self.croupier} :  {self.croupier.main}"])  #basé sur sa décision définit dans la classe du croupier
        
        self.perf_counter(time.perf_counter(), t_croupier_décide, "décision")
        self.inVerbose([f"{"-"*50}  RESULTAT DE LA PARTIE {"-"*50}"])
        ### === On affiche les vainqueurs et perdants de la partie ===
        self.inVerbose(["-"*50, "Détermination des vainqueurs", "-" * 50])
        t_gagnant = time.perf_counter()
        for joueur in self.joueurs:
            self.win(joueur)
            if joueur.main.result == 'gagné':
                self.tapis.compte.virement(joueur.mise, joueur)
                self.croupier.compte.virement(joueur.mise,joueur)
            elif joueur.main.result == 'égalisé':
                self.tapis.compte.virement(joueur.mise, joueur)
            else:
                self.tapis.compte.virement(joueur.mise, self.croupier)
            print(f"solde  {joueur} : {joueur.compte.montant}")
            self.inVerbose([f"{joueur} a {joueur.main.result}"])
        print(f"solde  {self.croupier} : {self.croupier.compte.montant}" )
        self.perf_counter(time.perf_counter(), t_gagnant, "pour déterminer gagnants")
        
        self.inVerbose([f"{"-"*50}  FIN DE LA PARTIE {"-"*50}"])

## === Fonctions secondaire ===
    def ramasser_main(self):
        #### === On ramasse les cartes de tous les joueurs et du croupier ===
        for joueur in self.joueurs + [self.croupier]: 
            joueur.main.défausser(self.deck.fausse) #fonction de la classe main pour défausser directement
            self.inVerbose([f"{joueur} apres défaussage :  {joueur.main}"])
        self.inVerbose(["Cartes ramassées."]) 
        return True
    ### === Fonction utilisée pour le tour de table dans la phase 1 (lancement) ===
    def tour_de_table(self): 
        #### === On distribue une carte à chaque joueur ===
        for joueur in self.liste_joueur_debout: 
            self.distribuer_carte(joueur) 
            ##### === Gestion du blackjack first shot ===
            if joueur.main.valeur ==21:
                joueur.est_couché = True
        return True 
    ### === Fonction pour distribuer une carte au joueur voulu ===
    def distribuer_carte(self, joueur:Joueur): 
        self.deck.inserer_dans(joueur.main, à_insérer=self.deck.tirer())
        return True 
    ### === Fonction de gestion de la victoire (gagné/perdu) ===
    def win(self, joueur : Joueur):
        #### === On récupère la valeur de la main ===
        valeur = joueur.main.valeur
        croupier_valeur = self.croupier.main.valeur
            ##### === Gestion des mains a double valeur (celle avec un As) ===
        if not(type(valeur) == int): #si il y a deux valeurs possible, on prend le max de celles ci 
            valeur = max(valeur)
        if not(type(croupier_valeur)==int):
            croupier_valeur = max(croupier_valeur)
        #### === Comparaison des mains du joueur et du croupier ===
        if valeur <= 21: #SI on a pas bust
            #Si on dépasse le croupier ou si le coupier a bust on gagne
            if valeur > croupier_valeur  or croupier_valeur > 21:
                result = "gagné"
            #Egalité
            elif valeur == croupier_valeur:
                result = "égalisé"
            #Si on dépasse pas le croupier et que le croupier a pas bust
            else: result = "perdu"
        else: #Si on a bust
            result = "perdu"
        joueur.main.result = result

## === Fonctions de Mise ===
    def miser(self):
        for joueur in self.joueurs:
            joueur.compte.virement(joueur.mise, self.tapis)
            
## === Fonctions pour une autre version du jeu ===
    def décisions_phase_2(self):
        self.inVerbose([f"{"-"*50}  DECISIONS DES JOUEURS {"-"*50}"])
        while not(self.liste_joueur_debout):
            self.décisions() 
            for joueur in self.liste_joueur_debout: 
               self.inVerbose([f"{joueur}  : {joueur.main}"]) 
    def décisions(self):
        for joueur in self.liste_joueur_debout:
            if joueur.choix == "auto":
                decision = joueur.décision() 
                self.tirer_ou_se_coucher(joueur, decision)
            else:
                self.tirer_ou_se_coucher(joueur, joueur.choix)
        return True 

        
            

