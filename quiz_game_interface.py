from quiz_game import QuizGame
from sys import exit
import pygame

BACKGROUND = "images/main_menu_background.jpg"
FONT = "Helvetica"
QUESTION_FONT_SIZE = 25
QUESTION_COORD = (100, 100)
ANSWER_FONT_SIZE = 13


class GameInterface:
    def __init__(self, screen, window_size):
        self.screen = screen
        self.window_size = window_size
        self.initialize_game()
        self.run()

    def initialize_game(self):
        self.question_font = pygame.font.SysFont(FONT, QUESTION_FONT_SIZE)
        self.answer_font = pygame.font.SysFont(FONT, ANSWER_FONT_SIZE)
        self.game = QuizGame()
        self.question_generator = self.game.get_next_question()

    def next_question(self):
        self.question = next(self.question_generator)
        return self.question

    def run(self):
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
                    pass

    def ask_question(self):
        self.question_surface = self.question_font.render(self.question.text,
                                                          True, (0, 255, 255))
        self.screen.blit(self.question_surface, QUESTION_COORD)

        for answer in self.question.answers:
            answer_surface = self.answer_font.render(answer.text, True,
                                                     (255, 255, 255))
            self.screen.blit(answer_surface, (300, 300))

        self.get_answer()
