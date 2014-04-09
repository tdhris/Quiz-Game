import pygame


class Button:
    def __init__(self, text):
        self.text = text
        self.is_hover = False
        self.default_color = (100, 100, 100)
        self.hover_color = (255, 255, 255)
        self.font_color = (0, 0, 0)
        self.surface = None

    def label(self):
        '''button label font'''
        font = pygame.font.Font(None, 20)
        return font.render(self.text, 1, self.font_color)

    def color(self):
        '''change color when hovering'''
        if self.is_hover:
            return self.hover_color
        else:
            return self.default_color

    def draw(self, screen, mouse, rectcoord, labelcoord):
        '''create rect button, draw, and change color based on input'''
        self.surface = pygame.draw.rect(screen, self.color(), rectcoord)
        screen.blit(self.label(), labelcoord)

        #change color if mouse over button
        self.check_hover(mouse)

    def check_hover(self, mouse):
        '''adjust is_hover value based on mouse over button
        - to change hover color'''
        self.is_hover = self.surface.collidepoint(mouse)
        return self.is_hover
