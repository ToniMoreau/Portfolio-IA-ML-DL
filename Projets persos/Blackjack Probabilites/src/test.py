from classes import *
from PIL import Image, ImageTk

import customtkinter as ctk
from PIL import Image, ImageTk


paquet = Paquet()
fausse = TasDeCartes()
deck = Deck(fausse=None)
deck.ajouter(paquet.cartes)
deck.attribuer_fausse(fausse)
deck.shuffle_stop()

main = Main()
tas = []
for i in range(6):
    tas += [deck.tirer()]
main.ajouter(tas)
print(main)
print(main.valeurs())


    


