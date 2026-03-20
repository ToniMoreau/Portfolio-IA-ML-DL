from joueurs.player import Player


class IAPlayer(Player):
    def __init__(self, nom, prenom):
        super().__init__(nom, prenom)
        
    def choose_action(self, actions):
        pass