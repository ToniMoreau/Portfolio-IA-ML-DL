
from joueurs import IAPlayer, ConsoleHumanPlayer, PyGameHumanPlayer
from renderer import ConsoleRenderer
from santorini import Santorini

Thomas = ConsoleHumanPlayer("Ide", "Thomas")
Toni = ConsoleHumanPlayer("Moreau", "Toni")

renderer = ConsoleRenderer()
jeu = Santorini([Thomas, Toni], renderer)


jeu.lancer_jeu()


