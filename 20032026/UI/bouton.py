import pygame

class Bouton:      
    def __init__(self, x, y, w, h, text, callback, FONT : pygame.font.Font,
                 color=(70, 130, 180),
                 hover_color=(100, 160, 210),
                 pressed_color=(50, 110, 160),
                 text_color=(255, 255, 255),
                 border_radius=12):
        self.FONT = FONT
        self.rect = pygame.Rect(x, y, w, h)
        self.text = text
        self.callback = callback

        self.color = color
        self.hover_color = hover_color
        self.pressed_color = pressed_color
        self.text_color = text_color
        self.border_radius = border_radius

        self.is_hovered = False
        self.is_pressed = False

    def handle_event(self, event : pygame.event.Event):
        callback = None
        if event.type == pygame.MOUSEMOTION:
            self.is_hovered = self.rect.collidepoint(event.pos)
            callback = None
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1 and self.rect.collidepoint(event.pos):
                self.is_pressed = True
                callback = None
                
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                if self.is_pressed and self.rect.collidepoint(event.pos):
                    callback = self.callback()
                self.is_pressed = False
        return callback

    def draw(self, surface : pygame.surface.Surface):
        if self.is_pressed:
            current_color = self.pressed_color
        elif self.is_hovered:
            current_color = self.hover_color
        else:
            current_color = self.color

        # ombre légère
        shadow_rect = self.rect.move(3, 3)
        pygame.draw.rect(surface, (30, 30, 30), shadow_rect, border_radius=self.border_radius)

        # bouton
        pygame.draw.rect(surface, current_color, self.rect, border_radius=self.border_radius)

        # contour
        pygame.draw.rect(surface, (255, 255, 255), self.rect, width=2, border_radius=self.border_radius)

        # texte centré
        text_surf = self.FONT.render(self.text, True, self.text_color)
        text_rect = text_surf.get_rect(center=self.rect.center)
        surface.blit(text_surf, text_rect)
