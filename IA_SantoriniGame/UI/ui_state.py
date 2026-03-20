import pygame

class UIState:
    def __init__(self):
        self.taille_case = 100
        self.taille_pion = 20
        self.nb_cases = 5
        self.mouse_pos = None
        
        self.SABLE = 230, 212, 194
        self.title_font = pygame.font.SysFont(None, 36)
        self.BLUE_SANTORINI = "#2F6FAF"
