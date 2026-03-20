from core.gameState import GameState
from renderer.renderer import Renderer
from UI.objets import *
from UI import UIState, Bouton

import pygame
class PyGameRenderer(Renderer):
    def __init__(self, screen : pygame.Surface):
        super().__init__()
        self.screen = screen
        self.ui_state = UIState()
        
        self.init_boutons()
    
    def init_boutons(self):
        self.jouer_btn = Bouton(400, 200, 120, 60, "Jouer", lambda : "SELECT_NB_JOUEURS", self.ui_state.title_font)
        self.quitter_btn = Bouton(400, 400, 120, 60, "Quitter",lambda : "QUITTER", self.ui_state.title_font)
        self.deux_joueurs_btn = Bouton(400, 200, 120, 60, "2 joueurs",lambda : "DEUX_JOUEURS", self.ui_state.title_font)
        self.retour_btn = Bouton(400, 400, 120, 60, "Retour",lambda : "MENU", self.ui_state.title_font)
        self.cases = cases_bouttons(self.ui_state)


    def render(self, state : GameState) -> list[Bouton]:
        phase = state.current_phase
        if phase =="MENU":
            return self.render_menu_principal(state)
        elif phase == "SELECT_NB_JOUEURS":
            return self.render_jouer_clicked(state)
        elif phase == "PLACEMENT":
            return self.render_placement(state)
    
    def render_placement(self, state):
        text_menu_surface = self.ui_state.title_font.render("Phase de Placement !", True, (0, 0, 0))
        self.screen.blit(text_menu_surface,(400,100))

        self.render_plateau(state)
        for case in self.cases:
            case.draw(self.screen)
        
        self.quitter_btn.draw(self.screen)
        
        boutons = self.cases.copy()
        boutons.append(self.quitter_btn)
    
        return boutons

    def render_plateau(self, state : GameState):
        dessiner_plateau(self.screen, self.ui_state)
        dessiner_pions(self.screen,state.worker_pos_by_worker.values() ,self.ui_state)
        return []
    
    def render_menu_principal(self,state : GameState):
        text_menu_surface = self.ui_state.title_font.render("Bienvenue Sur Santorini !", True, (0, 0, 0))
        self.screen.blit(text_menu_surface,(400,100))
        
        self.jouer_btn.draw(self.screen)
        
        self.quitter_btn.draw(self.screen)
        
        return [self.jouer_btn, self.quitter_btn]      
    
    def render_jouer_clicked(self, state : GameState):
        text_jouer_surface = self.ui_state.title_font.render("Selectionner le nombre de joueur :", True, (0, 0, 0))
        self.screen.blit(text_jouer_surface,(400,100))
        
        self.deux_joueurs_btn.draw(self.screen)
        
        self.retour_btn.draw(self.screen)
        
        return [self.deux_joueurs_btn, self.retour_btn]      
    
    def render_plateau(self, state : GameState):
        dessiner_plateau(self.screen, self.ui_state)
        dessiner_pions(self.screen, state.worker_pos_by_worker.values(), self.ui_state)
        

        
