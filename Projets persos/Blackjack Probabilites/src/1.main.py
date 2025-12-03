from classes import Paquet, Deck
from blackjack import BlackJack
from banque import Compte
from personnage import Joueur, Croupier, Entité
from visuel import *
import warnings
warnings.filterwarnings("ignore", message=".*CTkLabel Warning.*")
# === Bienvenue dans le main, la ou tout est exécuté ===
    ## === Création des paquets de cartes qui formeront le deck ===
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

    ## === Création des joueurs et du croupier ===
croupier = Croupier(3, "Croupier")
croupier_compte = Compte(montant=10000,proprietaire=croupier)
croupier.compte = croupier_compte

Toni = Joueur(1, "Roro")
Toni_compte = Compte(1000,Toni)
Toni.compte = Toni_compte
Tom = Joueur(2, "Toto")
Tom_compte = Compte(1000,Tom)
Tom.compte = Tom_compte



    ## === Création du jeu en y insérant les joueurs, le croupier, et le deck= ===
blackjack = BlackJack(croupier, joueurs=[Toni, Tom], deck=deck)

    # === Lancement de l'app du jeu ===
if __name__ == "__main__":
    app = App(blackjack)
    app.mainloop()
