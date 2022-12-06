import pygame
from sudoku_generator import generate_sudoku
pygame.init()

width, height = 900, 500
win = pygame.display.set_mode((width, height))
pygame.display.set_caption("Sudoku")

pencil = pygame.image.load("assets/pencil.png")
default_cursor = pygame.image.load("assets/cursor.png")
hand = pygame.image.load("assets/hand.png")
game_board = pygame.image.load("assets/grid.png")
home_background = pygame.image.load("assets/brain_code.jpg")

green = (57, 255, 20)
white = (255, 255, 255)
black = (0, 0, 0)
light_blue = (209, 237, 242)
grey = (80, 80, 80)
red = (255, 0, 0)
blue = (0, 0, 120)

cell_size = 48
empty_cells = 0
clickable = False
cell_num = 0
enter = False
user_num = ""
screen = "home"
arrow = ""

# start at y = 34 x = 234
fps = 244

class Font():
    def __init__(self, font_size = 16):
        self.font = pygame.font.Font("assets/arial.ttf", font_size)

    def get_font(self):
        return self.font

    def update_font_size(self, font_size):
        self.font = pygame.font.Font("assets/arial.ttf", font_size)

tiny_text = Font(8)
small_text = Font()
medium_text = Font(24)
big_text = Font(36)
bigger_text = Font(42)
title_text = Font(48)


class Button():
    def __init__(self, x, y, w, h, font = small_text, text = "", clickable = True, border = 2, color1 = green, color2 = black, color3 = green, centered = True):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.font = font
        self.text = text
        self.clickable = clickable
        self.border = border
        self.color1 = color1
        self.color2 = color2
        self.color3 = color3
        self.centered = centered

    def draw_button(self):
        pygame.draw.rect(win, self.color3, pygame.Rect(self.x, self.y, self.w, self.h))
        pygame.draw.rect(win, self.color2, pygame.Rect(self.x + self.border, self.y + self.border, self.w - self.border*2, self.h - self.border*2))
        display_text(self.text, self.x + self.w/2, self.y + self.h/2, self.font, self.color1, None, self.centered)

    def hovering(self, x, y):
        if x > self.x and x < self.x + self.w and y > self.y and y < self.y + self.h and self.clickable:
            return True
        return False

    def get_centered(self):
        return self.centered

    def get_clickable(self):
        return self.clickable

    def set_text(self, text, centered = True):
        self.text = text
        self.centered = centered

    def get_text(self):
        return self.text

    def set_color1(self, color):
        self.color1 = color

    def get_color1(self):
        return self.color1

    def set_color3(self, color):
        self.color3 = color

current_button = Button(0, 0, 0, 0)



easy_button = Button(width / 2 - 120, height / 2 -20, 240, 60, big_text, "Easy")
medium_button = Button(width / 2 - 120, height / 2 + 60, 240, 60, big_text, "Medium")
hard_button = Button(width / 2 - 120, height / 2 + 140, 240, 60, big_text, "Hard")
exit_button = Button(width / 2 - 180, height / 2 , 360, 90, bigger_text, "Exit")
restart_button = Button(width / 2 - 180, height / 2 , 360, 90, bigger_text, "Restart")
exit_button = Button(width / 2 - 180, height / 2 , 360, 90, bigger_text, "Exit")
reset_game_button = Button(width / 2 + 260, height / 2 -80, 120, 40, medium_text, "reset", True, 2, black, light_blue,black)
restart_game_button = Button(width / 2 + 260, height / 2 + 0, 120, 40, medium_text, "restart", True, 2, black, light_blue,black)
exit_game_button = Button(width / 2 + 260, height / 2 + 80, 120, 40, medium_text, "exit", True, 2, black, light_blue,black)


# displays text at center (x, y)
def display_text(text, x, y, font = small_text, color = black, background = None, centered = True):
    if centered:
        text = font.get_font().render(text, True, color, background)
        textCenter = text.get_rect(center=(x, y))
        win.blit(text, textCenter)
    else:
        text = small_text.get_font().render(text, True, color, background)
        textCenter = text.get_rect(center = (x-cell_size/2 + 8, y+cell_size/2 - 8))
        win.blit(text, textCenter)

def update_cursor(x,y, cursor = default_cursor):
    win.blit(cursor, (x, y))

class Board:
    def __init__(self, empty_cells):
        self.board = generate_sudoku(9, empty_cells)

    def create_buttons(self):
        x = 234
        y = 34
        self.grid_list = []
        i = 0
        j = 0
        while i < 9:
            while j < 9:
                clickable = False
                if self.board[i][j] == 0:
                    self.board[i][j] = ""
                    clickable = True
                new_button = Button(x, y, cell_size, cell_size, medium_text, str(self.board[i][j]), clickable, 1, black, white, black, True)
                self.grid_list.append(new_button)
                x += cell_size
                j += 1
            x = 234
            y += cell_size
            j = 0
            i += 1

    def update_buttons(self, current = -1):
        i = 0
        while i < 81:
            self.grid_list[i].draw_button()
            i += 1
        pygame.draw.rect(win, black, pygame.Rect(377, 35, 4, 434))
        pygame.draw.rect(win, black, pygame.Rect(521, 35, 4, 434))
        pygame.draw.rect(win, black, pygame.Rect(234, 176, 434, 4))
        pygame.draw.rect(win, black, pygame.Rect(234, 321, 434, 4))
        if current != -1:
            self.grid_list[current].draw_button()
    def clear_board(self):
        i = 0
        while i < 81:
            if self.grid_list[i].get_color1() != black:
                self.grid_list[i].set_text("")
                y = i % 9
                x = i // 9
                self.board[x][y] = ""
            i += 1



    def get_grid_list_button(self, i):
        return self.grid_list[i]

    def set_grid_list_button(self, i, button):
        self.grid_list[i] = button

    def submit_button(self, i, value):
        y = i % 9
        x = i // 9
        self.board[x][y] = int(value)
        empty = False
        h = 0
        j = 0
        while h < 9:
            while j < 9:
                if self.board[h][j] == "":
                    empty = True
                j += 1
            h += 1
            j = 0
        if not empty:
            return self.check_if_valid()
        else:
            return "game"



    def check_if_valid(self):
        global screen
        i = 0
        j = 0
        while i < 9:
            while j < 9:
                current_val = self.board[i][j]
                if not (self.check_row(i, current_val) and self.check_col(j, current_val) and self.check_box(i, j, current_val)):
                    return "game_lose"
                j += 1
            i += 1
            j = 0
        return "game_win"


    def check_row(self, row, value):
        i = 0
        count = 0
        while i < 9:
            if self.board[row][i] == value:
                count += 1
                if count >= 2:
                    return False
            i+= 1
        return True

    def check_col(self, col, value):
        i = 0
        count = 0
        while i < 9:
            if self.board[i][col] == value:
                count += 1
                if count >= 2:
                    return False
            i += 1
        return True

    def check_box(self, row, col, value):
        count = 0
        if row // 3 == 0:
            row_start = 0

        if row // 3 == 1:
            row_start = 3

        if row // 3 == 2:
            row_start = 6

        if col // 3 == 0:
            col_start = 0

        if col // 3 == 1:
            col_start = 3

        if col // 3 == 2:
            col_start = 6

        i = row_start
        j = col_start
        while i < row_start + 3:
            while j < col_start + 3:
                if self.board[i][j] == value:
                    count += 1
                if count >= 2:
                    print("Check box")
                    return False
                j += 1
            j = col_start
            i += 1
        return True

def draw_screen(screen):
    global empty_cells
    global board
    global num_input
    global clickable
    global current_button
    global cell_num
    global enter
    global user_num
    global arrow

    x, y = pygame.mouse.get_pos()
    if screen == "home":
        win.fill(white)
        win.blit(home_background, (0, -30))
        easy_button.draw_button()
        medium_button.draw_button()
        hard_button.draw_button()
        display_text("Welcome to Sudoku", width/2, 80, title_text, black, white)
        display_text("Select Game Mode:", width/2, 180, big_text, black, white)

        if easy_button.hovering(x + 5, y) or medium_button.hovering(x + 5, y) or hard_button.hovering(x + 5, y):
            update_cursor(x, y, hand)
            if mouse_click:
                if easy_button.hovering(x + 5, y):
                    empty_cells = 30
                elif medium_button.hovering(x + 5, y):
                    empty_cells = 40
                else:
                    empty_cells = 50
                board = Board(empty_cells)
                board.create_buttons()
                screen = "game"
        else:
            update_cursor(x, y, default_cursor)

    if screen == "game":
        win.fill(light_blue)
        win.blit(game_board, (225, 25))
        reset_game_button.draw_button()
        restart_game_button.draw_button()
        exit_game_button.draw_button()
        board.update_buttons()
        if restart_game_button.hovering(x, y):
            update_cursor(x, y, hand)
            if mouse_click:
                screen = "home"
        elif reset_game_button.hovering(x, y):
            update_cursor(x, y, hand)
            if mouse_click:
                board.clear_board()
                user_num = ""

        elif exit_game_button.hovering(x, y):
            update_cursor(x,y, hand)
            if mouse_click:
                exit()
        else:
            update_cursor(x, y-24, pencil)
            if mouse_click:
                num_input = False
                enter = False
                current_button.set_color3(black)

                cell_num = ((x-234) // cell_size) + ((y - 34) // cell_size) * 9
                if cell_num < 81:
                    current_button = board.get_grid_list_button(cell_num)


            if arrow != "":
                user_num = ""
                num_input = False
                if arrow == "up":
                    if cell_num >= 9:
                        current_button.set_color3(black)
                        cell_num -= 9
                        current_button = board.get_grid_list_button(cell_num)
                elif arrow == "down":
                    if cell_num < 72:
                        current_button.set_color3(black)
                        cell_num += 9
                        current_button = board.get_grid_list_button(cell_num)
                elif arrow == "left":
                    if cell_num % 9 != 0:
                        current_button.set_color3(black)
                        cell_num -= 1
                        current_button = board.get_grid_list_button(cell_num)
                elif arrow == "right":
                    if cell_num % 9 != 8:
                        current_button.set_color3(black)
                        cell_num += 1
                        current_button = board.get_grid_list_button(cell_num)
                arrow = ""
            clickable = current_button.get_clickable()

            if clickable:
                current_button.set_color3(red)
                board.update_buttons(cell_num)
                update_cursor(x, y - 24, pencil)
                sketched_text = current_button.get_text()
                if num_input:
                    current_button.set_text(str(user_num), False)
                    current_button.set_color1(grey)
                    board.set_grid_list_button(cell_num, current_button)
                if enter:
                    num_input = False
                    user_num = ""
                    if sketched_text != "":
                        current_button.set_color1(blue)
                        current_button.set_text(sketched_text, True)
                        current_button.set_color3(blue)
                        board.set_grid_list_button(cell_num, current_button)
                        screen = board.submit_button(cell_num, sketched_text)
                    enter = False


    if screen == "game_lose":
        win.fill(white)
        win.blit(home_background, (0, -30))
        restart_button.draw_button()
        display_text("Game Over :(", width / 2, 120, title_text, black, white)

        if restart_button.hovering(x + 5, y):
            update_cursor(x, y, hand)
            if mouse_click:
                screen = "home"
        else:
            update_cursor(x,y)
    if screen == "game_win":
        win.fill(white)
        win.blit(home_background, (0, -30))
        exit_button.draw_button()
        display_text("Game Won!!!", width / 2, 120, title_text, black, white)

        if exit_button.hovering(x + 5, y):
            update_cursor(x, y, hand)
            if mouse_click:
                exit()
        else:
            update_cursor(x, y)

    pygame.display.update()
    return screen


def main():
    global screen
    global mouse_click
    global num_input
    global user_num
    global enter
    global arrow

    num_input = False
    mouse_click = False
    clock = pygame.time.Clock()
    pygame.mouse.set_visible(False)
    run = True
    while run:
        clock.tick(fps)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            mouse_click = True if event.type == pygame.MOUSEBUTTONDOWN else False
            if event.type == pygame.KEYDOWN:
                num_input = True
                if event.key == pygame.K_1 or event.key == pygame.K_KP1:
                    user_num = 1
                if event.key == pygame.K_2 or event.key == pygame.K_KP2:
                    user_num = 2
                if event.key == pygame.K_3 or event.key == pygame.K_KP3:
                    user_num = 3
                if event.key == pygame.K_4 or event.key == pygame.K_KP4:
                    user_num = 4
                if event.key == pygame.K_5 or event.key == pygame.K_KP5:
                    user_num = 5
                if event.key == pygame.K_6 or event.key == pygame.K_KP6:
                    user_num = 6
                if event.key == pygame.K_7 or event.key == pygame.K_KP7:
                    user_num = 7
                if event.key == pygame.K_8 or event.key == pygame.K_KP8:
                    user_num = 8
                if event.key == pygame.K_9 or event.key == pygame.K_KP9:
                    user_num = 9
                if event.key == pygame.K_RETURN:
                    enter = True
                if event.key == pygame.K_UP:
                    arrow = "up"
                if event.key == pygame.K_DOWN:
                    arrow = "down"
                if event.key == pygame.K_RIGHT:
                    arrow = "right"
                if event.key == pygame.K_LEFT:
                    arrow = "left"

        screen = draw_screen(screen)

    pygame.quit()

if __name__ == "__main__":
    main()
