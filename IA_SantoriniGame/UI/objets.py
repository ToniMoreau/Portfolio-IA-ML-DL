import pygame
from .ui_state import UIState
from .bouton import Bouton

def dessiner_plateau(surface, ui_state : UIState):
    taille_case = ui_state.taille_case
    for i in range(ui_state.nb_cases):
        for j in range(ui_state.nb_cases):
            pygame.draw.rect(surface, (0,0,0),(taille_case*j,taille_case*i,taille_case,taille_case), 2, 2)
            
def cases_bouttons(ui_state : UIState) -> list[Bouton]:
    boutons = []
    taille_case = ui_state.taille_case
    for i in range(ui_state.nb_cases):
        for j in range(ui_state.nb_cases):
            btn = Bouton(taille_case*j,taille_case*i,taille_case,taille_case, f"({i},{j})",lambda a= i, b=j : (a,b) ,ui_state.title_font)
            boutons.append(btn)
    return boutons
    
    
def dessiner_pions(surface, pions_pos, ui_state : UIState):
    if pions_pos:
        for pion_pos in pions_pos:
            if pion_pos is None:
                pass
            else:
                left, top, width, height = get_case_from_pion_pos(pion_pos, ui_state)
                pygame.draw.circle(surface, (255,0,0), (left+width/2, top+height/2),ui_state.taille_pion)
        
    else:
        pass
        
def get_case_from_pion_pos(pion_pose, ui_state : UIState):
    taille_case = ui_state.taille_case
    top,left = pion_pose
    return (left*taille_case, top*taille_case, taille_case, taille_case)

def pion_sur_case_clique(pions, mouse_pos, ui_state : UIState):    
    if mouse_pos:
        for pion in pions:
            left, top, width, height = get_case_from_pion_pos(pion, ui_state)
            case = pygame.Rect(left, top, width, height)
            if case.collidepoint(mouse_pos):
                return case
        return None
    else:
        return None
    
def colore_si_pion(surface, case, color):
    if case:
        pygame.draw.rect(surface, color, case, border_radius=2, width= 5)

        
def deplacement_pion(surface, case_pion, actions, ui_state : UIState):
    if case_pion : 
        for action in actions:
            case = get_case_from_pion_pos(action.move_to_pos)
            pygame.draw.rect(surface, (0,255,0), case, width=5)
            
    