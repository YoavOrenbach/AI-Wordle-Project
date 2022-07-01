import pygame
import string

pygame.init()
pygame.font.init()
FONT = pygame.font.Font('freesansbold.ttf', 22)
GREEN, YELLOW, GREY, BLACK, WHITE = (107, 241, 83), (228, 208, 10), (163, 163, 157), (0, 0, 0), (255, 255, 255)
AVAILABLE_LETTERS = [letter for letter in string.ascii_uppercase]


class Grid:
    """
    Implement a Grid class to add one more layer of abstraction
    """
    def __init__(self):
        self.matrix = [[Cell(i, j) for j in range(5)] for i in range(6)]
        self.current_row, self.current_column = 0, 0

    def enter_letter(self, letter):
        letter = letter.upper()
        if letter in AVAILABLE_LETTERS:
            if self.current_column == 5:  # user has already entered 5 letters
                print("Sorry Request cannot be processed")
                return
            self.matrix[self.current_row][self.current_column].assign_letter(letter)
            self.current_column += 1

    def submit_word(self, verdict):
        hash = {"g": GREEN, "b": GREY, "y": YELLOW}
        for j, cell in enumerate(self.matrix[self.current_row]):
            cell.process_associated_row(hash[verdict[j]])
        self.current_row += 1
        self.current_column = 0

    def draw(self, window):
        for row in self.matrix:
            for cell in row:
                cell.draw(window)


class Cell:
    def __init__(self, row, column):
        self.row = row
        self.column = column
        self.__assigned_letter = None
        self.__background_color = None
        self.x = (column + 1) * 80 - 20
        self.y = (row + 1) * 80 + 50
        self.size = 70

        # keeps track of whether the user is done with the row yet
        self.__processed_row = False

    def get_letter(self):
        return self.__assigned_letter

    def assign_letter(self, letter):  # assign the block a letter upon user input
        self.__assigned_letter = letter

    def remove_letter(self):  # removes the letter from the cell if the user presses backspace
        self.__assigned_letter = None

    def process_associated_row(self, verdict_color):
        self.__processed_row = True
        self.__background_color = verdict_color

    def draw(self, window):
        background_color = self.__background_color if self.__processed_row else GREY
        pygame.draw.rect(window, background_color,
                         (self.x, self.y, self.size, self.size))

        # if the associated row isn't processed yet, the cell should be white colored with grey borders
        if not self.__processed_row:
            pygame.draw.rect(window, WHITE, (self.x + 2, self.y +
                                             2, self.size - 4, self.size - 4))
        # display the letter on the cell
        # if the row is yet to be processed, meaning the user is currently
        # guessing on the associated row the text color should be black and white otherwise
        if self.__assigned_letter != None:
            text_color = BLACK if not self.__processed_row else WHITE
            text = FONT.render(self.__assigned_letter, False, text_color)
            window.blit(text, (self.x + 20, self.y + 19))


class GraphicalInterface:
    WIDTH, HEIGHT = (500, 700)

    def __init__(self, target_word):
        self.window = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("WORDLE REDEEMED")
        self.target_word = target_word
        self.sharable_verdict = []
        self.grid = Grid()
        self.render_graphics()

    def show_error_message(self, message):
        message_screen = FONT.render(message, False, (255, 0, 0))
        self.window.blit(message_screen, (90, 620))
        pygame.display.update()
        pygame.time.delay(500)

    def render_graphics(self):
        self.window.fill(WHITE)
        self.grid.draw(self.window)
        pygame.display.update()

    def generate_verdict(self, guessed_word):
        target_word_copy = [letter for letter in self.target_word]
        verdict = ['b' for i in range(5)]

        # first list out the correct letters in the correct spot
        for i in range(5):
            if target_word_copy[i] == guessed_word[i]:
                target_word_copy[i] = "*"
                verdict[i] = "g"

        # check for letters in the incorrect spots
        for i in range(5):  # outer loop for the guessed word
            if verdict[i] != "b":  # skip this letter if it's already in correct spot
                continue
            for j in range(5):  # inner loop for the target word
                if i == j or target_word_copy[j] == "*":
                    continue
                if guessed_word[i] == target_word_copy[j]:
                    target_word_copy[j] = "*"
                    verdict[i] = "y"
                    break
        self.sharable_verdict.append(verdict)
        return verdict

    def event_handler(self, guess):
        #print(f"TARGET WORD: {self.target_word}, guess: {guess}")
        for letter in guess:
            self.grid.enter_letter(letter)
        current_verdict = self.generate_verdict(guess)
        self.grid.submit_word(current_verdict)
        self.render_graphics()

    def load_ending_screen(self, win=True):
        message = ("YOU WON!" if win else "YOU LOST!") + f" THE WORD WAS: {self.target_word}"
        message_screen = FONT.render(message, False, (255, 0, 0))
        self.window.blit(message_screen, (65, 620))
        #self.window.blit(FONT.render("PRESS ANY KEY TO RESTART", False, (255, 191, 0)), (85, 80))
        pygame.display.update()
        pygame.display.quit()
        #pygame.quit()
