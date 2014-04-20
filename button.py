import pygame


class Button(pygame.sprite.Sprite):
    def __init__(self, label, default_image, hover_image, coordinates, function):
        pygame.sprite.Sprite.__init__(self)
        self.label = label
        self.default_image = pygame.image.load(default_image).convert_alpha()
        self.hover_image = pygame.image.load(hover_image).convert_alpha()
        self.coordinates = coordinates
        self.function = function
        self.is_hover = False
        self.surface = None

    def __eq__(self, other):
        return self.label == other.label and self.function == other.function

    @property
    def image(self):
        if self.is_hover:
            return self.hover_image
        else:
            return self.default_image

    def draw(self, screen, mouse):
        self.check_hover(mouse)
        screen.blit(self.image, self.coordinates)

    def check_hover(self, mouse):
        mouse_x, mouse_y = mouse
        button_x, button_y = self.coordinates
        width = self.image.get_width()
        height = self.image.get_height()
        x_inside = (mouse_x > button_x) and (mouse_x < button_x + width)
        y_inside = (mouse_y > button_y) and (mouse_y < button_y + height)
        self.is_hover = x_inside and y_inside
        return self.is_hover
