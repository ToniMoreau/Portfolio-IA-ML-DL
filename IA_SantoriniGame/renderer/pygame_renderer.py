from core.gameState import GameState
from renderer.renderer import Renderer
from UI.objets import *
from UI import UIState, BoutonByCenter

import pygame
class PyGameRenderer(Renderer):
    def __init__(self, screen : pygame.Surface):
        super().__init__()
        self.screen = screen
        self.ui_state = UIState()
        
        self.init_boutons()
    
    def init_boutons(self):
        self.ui_state.screen_height = self.screen.get_height()
        self.ui_state.screen_width = self.screen.get_width()
        
        
        #Bouton MENU:
        self.Mjouer_btn = BoutonByCenter(self.ui_state.screen_width*0.5, self.ui_state.screen_height * 0.3, 120, 60, "Jouer", lambda : "SELECT_NB_JOUEURS", self.ui_state.title_font)
        self.Mquitter_btn = BoutonByCenter(self.ui_state.screen_width*0.5, self.ui_state.screen_height * 0.6, 120, 60, "Quitter",lambda : "QUITTER", self.ui_state.title_font)
        
        #Bouton SELECTION JOUEURS
        self.deux_joueurs_btn = BoutonByCenter(self.ui_state.screen_width*0.5, self.ui_state.screen_height * 0.3, 120, 60, "2 joueurs",lambda : "DEUX_JOUEURS", self.ui_state.title_font)
        self.sj_retour_btn = BoutonByCenter(self.ui_state.screen_width*0.5, self.ui_state.screen_height * 0.6, 120, 60, "Retour",lambda : "MENU", self.ui_state.title_font)
        
        #Bouton IN GAME
        self.pions_btn = []
        self.GFin_btn = BoutonByCenter(self.ui_state.screen_width*0.75, self.ui_state.screen_height * 0.6, 120, 60, "Fin Partie.",lambda : "FIN", self.ui_state.title_font)
        self.active_case_buttons = [] 


    def render(self, state: GameState):
        phase = state.current_phase

        if phase == "MENU":
            return self.render_menu_principal(state)
        elif phase == "SELECT_NB_JOUEURS":
            return self.render_jouer_clicked(state)
        elif phase == "PLACEMENT":
            return self.render_placement(state)
        elif phase == "MOVE":
            return self.render_placement(state)
        elif phase == "BUILD":
            return self.render_placement(state)
        else:
            return self.render_menu_principal(state)  
          
    def render_placement(self, state: GameState):
        text_menu_surface = self.ui_state.title_font.render("Phase de Placement !", True, (0, 0, 0))
        text_menu_rect = text_menu_surface.get_rect(center = (self.ui_state.screen_width* 0.75, self.ui_state.screen_height * 0.1) )
        
        self.screen.blit(text_menu_surface, text_menu_rect)
        
        current_joueur_surface = self.ui_state.title_font.render(f"Au tour de : {state.current_player} !", True, (0,0,0))
        current_joueur_rect = current_joueur_surface.get_rect(center = (self.ui_state.screen_width* 0.75, self.ui_state.screen_height* 0.2) )
        self.screen.blit(current_joueur_surface, current_joueur_rect)
        
        self.render_plateau(state)
        
        self.GFin_btn.draw(self.screen)
        
        boutons = self.active_case_buttons.copy()
        boutons.extend(self.pions_btn)
        boutons.append(self.GFin_btn)
    
        return boutons

    def render_plateau(self, state : GameState):
        dessiner_plateau(self.screen, self.ui_state)
        dessiner_construction(self.screen,state, self.ui_state)
        

        if self.active_case_buttons:
            for case in self.active_case_buttons:
                case.draw(self.screen)
            
        for pion_btn in self.pions_btn:
            pion_btn.draw(self.screen)
        
        dessiner_pions(self.screen,state ,self.ui_state)
        
        return []
    
    def render_menu_principal(self,state : GameState):
        text_menu_surface = self.ui_state.title_font.render("Bienvenue Sur Santorini !", True, (0, 0, 0))
        text_menu_rect = text_menu_surface.get_rect(center = (self.ui_state.screen_width* 0.5, self.ui_state.screen_height* 0.1) )
        self.screen.blit(text_menu_surface,text_menu_rect)
        
        self.Mjouer_btn.draw(self.screen)
        
        self.Mquitter_btn.draw(self.screen)
        
        return [self.Mjouer_btn, self.Mquitter_btn]      
    
    def render_jouer_clicked(self, state : GameState):
        text_jouer_surface = self.ui_state.title_font.render("Selectionner le nombre de joueur :", True, (0, 0, 0))
        text_jouer_rect = text_jouer_surface.get_rect(center = (self.ui_state.screen_width* 0.5, self.ui_state.screen_height* 0.1) )

        self.screen.blit(text_jouer_surface,text_jouer_rect)
        
        self.deux_joueurs_btn.draw(self.screen)
        
        self.sj_retour_btn.draw(self.screen)
        
        return [self.deux_joueurs_btn, self.sj_retour_btn]      
        
    def update_active_case_buttons(self, allowed_cells):
        self.active_case_buttons = cases_bouttons_autorisees(allowed_cells, self.ui_state)
    
    def update_pion_buttons(self, state: GameState):
        self.pions_btn = pions_boutons(state, self.ui_state, self.ui_state.title_font)