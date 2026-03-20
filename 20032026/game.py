import pygame
import sys
from UI.objets import *
from UI.ui_state import UIState
import numpy as np
from core import GameState, SantoriniRules
from renderer import PyGameRenderer
from joueurs import PyGameHumanPlayer, Player
from santorini import Santorini
from UI import Bouton

##INITIALISATION de PYGAME et de la fenêtre, + temps
pygame.init()
screen = pygame.display.set_mode((800,600))
pygame.display.set_caption("Santorini")
background = pygame.Surface(screen.get_size())
clock = pygame.time.Clock()

##ETATS : UI + JEU
renderer = PyGameRenderer(screen)
rules = SantoriniRules()
gameState = GameState()

Toni = PyGameHumanPlayer("Moreau", "Toni")
Thomas = PyGameHumanPlayer("Ide", "Thomas")

santorini = Santorini([Toni,Thomas], renderer)

##MISE EN PLACE :
    #raccourcis instance
renderer : PyGameRenderer = santorini.renderer
players = santorini.players
    #mélange de l'ordre de passage
ordre_tour = list(range(len(players)))
np.random.shuffle(ordre_tour)

    #initialisation de l'état de jeu (tout à zéro)
state = santorini.rules.initial_state(ordre_tour)
state.current_phase = "MENU"


boutons : list[Bouton] = []
running = True
while running:
    # 1️⃣ Gérer les événements
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        for bouton in boutons:
            action = bouton.handle_event(event)
            if action == "DEUX_JOUEURS":
                state.nb_joueurs = 2
                state.current_phase = "PLACEMENT"
            elif action is None:
                pass
            elif action == "QUITTER":
                running = False
            elif type(action) == tuple:
                print(action)
            else:
                state.current_phase = action
           
    background.fill(renderer.ui_state.SABLE)  # fond blanc
    screen.blit(background, (0,0))
    
    boutons = renderer.render(state)
    
    """if state.current_phase == "PLACEMENT":
        renderer.render(state) #visuel initial sans placement
        state.current_phase = "PLACEMENT"
        state = santorini.phase_placement(state)
        print("Placement effectué.")
        state.current_phase = state.PHASES[0]
    else:
        p_id = state.current_player                             #id joueur courant
        player :Player = players[p_id]                          #selection du joueur selon l'id courant

        if state.current_phase == state.PHASES[0]:
            print(f"C'est à {player} de jouer !\n")
            
            actions = santorini.rules.legal_actions(state)      #récup les actions possibles du joueur courant
            
            if not actions:
                break
            
            action = player.choose_action(actions)              #Méthode qui permet au joueur de choisir l'action qu'il veut, peut importe le format (PyGame, Terminal,...)
            state = santorini.rules.apply_action(state, action) #Exécution de l'action.
            state.current_phase = santorini.rules.next_phase(state)

        elif state.current_phase == state.PHASES[-1]:
            actions = santorini.rules.legal_actions(state)      #récup les actions possibles du joueur courant
            
            if not actions:
                break
            
            action = player.choose_action(actions)              #Méthode qui permet au joueur de choisir l'action qu'il veut, peut importe le format (PyGame, Terminal,...)
            state = santorini.rules.apply_action(state, action) #Exécution de l'action.

            state.current_player = santorini.rules.next_player(state)
            state.current_phase = santorini.rules.next_phase(state)"""
            
    # 2️⃣ Mettre à jour la logique (optionnel)
    pygame.display.flip()

    # 5️⃣ Limiter le framerate
    clock.tick(60)  
    
pygame.quit()
sys.exit()