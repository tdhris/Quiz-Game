import pygame
from button import Button


class QuizGame:
    running = True

    def __init__(self, size):
        pygame.init()
        self.button = Button("New Game")
        self.screen = pygame.display.set_mode(size)
        self.set_background(size)
        self.run()

    def set_background(self, size):
        background = pygame.image.load("images/background.jpg").convert()
        self.background = pygame.transform.scale(background, size)
        self.screen.fill((200, 200, 200))
        self.screen.blit(self.background, (0, 0))

    def draw(self):
        self.button.draw(self.screen, self.mouse, (100, 100, 100, 20), (125, 103))
        pygame.display.update()

    def run(self):
        while self.running:
            self.mouse = pygame.mouse.get_pos()
            self.draw()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if self.button.check_hover(self.mouse):
                        print("yay, it works")
                        self.new_game()

    def new_game(self):
        pass

    def game_options(self):
        pass


if __name__ == '__main__':
    QuizGame((640, 480)).run()
