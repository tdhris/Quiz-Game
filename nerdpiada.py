import pygame
from sys import exit
from button import Button
from quiz_game import QuizGame


BACKGROUND = "images/main_menu_background.jpg"
WINDOW_SIZE = (640, 480)

NEW_GAME_BUTTON = "images/new_game_button.png"
NEW_GAME_HOVER_BUTTON = "images/new_game_button_pressed.png"
NEW_GAME_BUTTON_COORD = (100, 150)

OPTIONS_BUTTON = "images/options_button.png"
OPTIONS_HOVER_BUTTON = "images/options_button_pressed.png"
OPTIONS_BUTTON_COORD = (100, 200)

FONT = "Helvetica"
QUESTION_FONT_SIZE = 35
ANSWER_FONT_SIZE = 15
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)


class MainMenu:
    running = True

    def __init__(self, size):
        self.window_size = size
        pygame.init()
        self.screen = pygame.display.set_mode(self.window_size)
        self.set_buttons()
        self.set_background(self.window_size)
        self.run()

    def set_background(self, size):
        background = pygame.image.load(BACKGROUND).convert()
        self.background = pygame.transform.scale(background, size)
        self.screen.fill((200, 200, 200))
        self.screen.blit(self.background, (0, 0))

    def set_buttons(self):
        self.buttons = []
        #new game button
        new_game_button = Button("New Game",
                                 NEW_GAME_BUTTON,
                                 NEW_GAME_HOVER_BUTTON,
                                 NEW_GAME_BUTTON_COORD,
                                 self.new_game)
        self.buttons.append(new_game_button)

        #options button
        options_button = Button("Options",
                                OPTIONS_BUTTON,
                                OPTIONS_HOVER_BUTTON,
                                OPTIONS_BUTTON_COORD,
                                self.game_options)
        self.buttons.append(options_button)

    def draw(self):
        for button in self.buttons:
            button.draw(self.screen, self.mouse)
        pygame.display.update()

    def run(self):
        while self.running:
            self.mouse = pygame.mouse.get_pos()
            self.draw()

            #event handlers
            for event in pygame.event.get():
                #quitting the game
                if event.type == pygame.QUIT:
                    self.quit_game()
                #pressing a button
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    for button in self.buttons:
                        if button.check_hover(self.mouse):
                            self.clear_screen()
                            button.function()

    def new_game(self):
        self.initialize_quiz_game()
        self.run_quiz()

    def game_options(self):
        print("options")

    def quit_game(self):
        exit(0)

    '''QuizGame Interface Functions'''
    def initialize_quiz_game(self):
        self.question_font = pygame.font.SysFont('comicsansms',
                                                 QUESTION_FONT_SIZE)
        self.answer_font = pygame.font.SysFont(FONT, ANSWER_FONT_SIZE)
        self.game = QuizGame()
        self.question_generator = self.game.get_next_question()

    def next_question(self):
        self.question = next(self.question_generator)
        return self.question

    def run_quiz(self):
        quiz_running = True
        while quiz_running:
            self.mouse = pygame.mouse.get_pos()
            self.next_question()
            self.ask_question()

    def get_answer(self):
        answered = False
        while not answered:
            for event in pygame.event.get():
                #quitting the game
                if event.type == pygame.QUIT:
                    exit(0)
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    answered = True
                    self.clear_screen()

    def ask_question(self):
        self.question_surface = self.question_font.render(self.question.text,
                                                          True, WHITE)
        question_width = self.question_surface.get_width()
        question_height = self.question_surface.get_height()
        question_coord = (((WINDOW_SIZE[0] - question_width) // 2),
                          (int((WINDOW_SIZE[1] - question_height) * 0.3)))
        self.screen.blit(self.question_surface, question_coord)

        coord_generator = self.get_answer_coordinates()
        for answer in self.question.answers:
            answer_coordinates = next(coord_generator)
            answer_surface = self.answer_font.render(answer.text, True,
                                                     WHITE)
            self.screen.blit(answer_surface, answer_coordinates)

        pygame.display.flip()
        self.get_answer()

    def get_answer_coordinates(self):
        answer_coordinates = [(100, 200),
                              (100, 250),
                              (100, 300),
                              (100, 350)]
        for coord in answer_coordinates:
            yield coord

    def clear_screen(self):
        self.buttons = []
        self.set_background(self.window_size)
        self.draw()

if __name__ == '__main__':
    MainMenu(WINDOW_SIZE).run()
