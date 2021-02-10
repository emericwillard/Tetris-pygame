import pygame as pg
import random

pg.init()

screen = pg.display.set_mode((450, 600))

pg.font.init()

myfont = pg.font.SysFont('Comic Sans MS', 14)
myfont2 = pg.font.SysFont('Comic Sans MS', 22)

width = screen.get_width()
height = screen.get_height()

pg.display.set_caption("NewTetris-V1")

case = 30

white = (255, 255, 255)
black = (0, 0, 0)
green = (0, 255, 0)
red = (255, 0, 0)
blue = (0, 0, 255)
yellow = (255, 255, 0)
orange = (255, 165, 0)
pink = (255, 192, 203)

S = [['.....',
      '..00.',
      '.00..',
      '.....'],
     ['....',
      '.0..',
      '.00.',
      '..0.',
      '....'],
     ['.....',
      '.00..',
      '..00.',
      '.....'],
     ['....',
      '..0.',
      '.00.',
      '.0..',
      '....']
     ]
I = [['...',
      '.0.',
      '.0.',
      '.0.',
      '.0.',
      '...'],
     ['......',
      '.0000.',
      '......']]
O = [['....',
      '.00.',
      '.00.',
      '....']]
L = [['....',
      '.0..',
      '.0..',
      '.00.',
      '....'],
     ['.....',
      '.000.',
      '.0...',
      '.....'],
     ['....',
      '.00.',
      '..0.',
      '..0.',
      '....'],
     ['.....',
      '...0.',
      '.000.',
      '.....']]
K = [['.....',
      '..0..',
      '.000.',
      '.....'],
     ['....',
      '..0.',
      '.00.',
      '..0.',
      '....'],
     ['.....',
      '.000.',
      '..0..',
      '.....'],
     ['....',
      '.0..',
      '.00.',
      '.0..',
      '....']]

form = [S, I, O, L, K]
color = [blue, green, pink, orange, yellow]
l_mem = []
delay = 500
mult_d = 1.5
result = 0
lost = False


class draw_form:

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.form = random.choice(form)
        self.position = 0
        self.color = color[form.index(self.form)]

    def get_form(self, on_display=True):
        if on_display:
            l = []
            sx = self.x
            sy = self.y
            for i in range(len(self.form[self.position])):
                for j in range(len(self.form[self.position][i])):
                    if self.form[self.position][i][j] == '0':
                        l.append(pg.Rect(sx, sy, 29, 29))
                    sx += 30
                sx = self.x
                sy += 30
            return l

    def set_position(self):
        self.position = (self.position + 1) % len(self.form)

    def get_height(self):
        h = 0
        for i in self.form[self.position]:
            if "0" in i:
                h += 30
        return h

    def get_width(self):
        max = 0
        for i in range(len(self.form[self.position])):
            w = 0
            for j in range(len(self.form[self.position][i])):
                if self.form[self.position][i][j] == "0":
                    w += 1
            if w > max:
                max = w
        return max


def draw_grid():
    for i in range(1, 21):
        pg.draw.line(screen, white, (0, i * case), (300, i * case), 1)
    for i in range(0, 11):
        pg.draw.line(screen, white, (i * case, 0), (i * case, 600), 1)


def check_case(f):
    for i in range(len(l_mem)):
        for j in f.get_form():
            for k in l_mem[i]:
                if k.y == j.y + 30 and k.x == j.x:
                    return True
    return False


def check_victory():
    d_vict = {}
    l = []
    for i in l_mem:
        for j in i:
            if not j.y in d_vict:
                d_vict[j.y] = [j.x]
            else:
                d_vict[j.y].append(j.x)
            if len(d_vict[j.y]) == 10:
                l.append(j.y)
                d_vict.pop(j.y)
    return l


def check_lost():
    for i in l_mem:
        for j in i:
            if j.y <= 1:
                return True
    return False


def check_best(r):
    with open('best_result', 'r') as f:
        best = int(f.readlines()[0])
        if r >= best:
            with open('best_result', 'w') as f:
                f.write(str(r))
                return True
    return False


def main():
    global f, delay, l_mem, result, mult_d, lost
    list_form = []
    key_push = False
    new_form = True
    running = True
    while running:
        if not lost:
            if new_form:
                f = draw_form(91, -29)
                f.get_form()
                list_form.append(f)
                new_form = False

            for event in pg.event.get():
                key_push = True
                if event.type == pg.QUIT:
                    running = False
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_LEFT:
                        if f.x - 30 != -59:
                            f.x -= 30
                    elif event.key == pg.K_RIGHT:
                        if f.x + 30 < 271 - (f.get_width() * 10):
                            f.x += 30
                    elif event.key == pg.K_DOWN:
                        if f.y + 30 != 571 - f.get_height():
                            f.y += 30
                    elif event.key == pg.K_UP:
                        f.set_position()
                    elif event.key == pg.K_c:
                        pg.time.delay(20000)
                    f.get_form()

            if not key_push:
                pg.time.delay(delay)
                if f.y != 571 - f.get_height():
                    if not check_case(f):
                        f.get_form()
                        f.y += 30
                    else:
                        list_form[list_form.index(f)] = f
                        new_form = True
                        l_mem.append(f.get_form())
                else:
                    list_form[list_form.index(f)] = f
                    new_form = True
                    l_mem.append(f.get_form())
            else:
                key_push = False
            screen.fill(black)
            cv = check_victory()
            lost = check_lost()
            count = 0
            complete_row = False
            for i in range(len(list_form)):
                for j in list_form[i].get_form():
                    if j.y not in cv:
                        pg.draw.rect(screen, list_form[i].color, j)
                    else:
                        complete_row = True
                        count += 1
            if complete_row:
                delay = int(delay / mult_d)
                mult_d = mult_d * 0.95
                if (delay < 1):
                    delay = 1
                result = result + count
                new_form = True
                l_mem = []
                list_form = []
            score = myfont.render('score : {}'.format(result), False, white)
            screen.blit(score, (310, 100))
            draw_grid()
            pg.display.update()
        else:
            for event in pg.event.get():
                screen.fill(blue)
                if event.type == pg.QUIT:
                    running = False
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_SPACE:
                        running = True
                        list_form = []
                        l_mem = []
                        result = 0
                        delay = 500
                        mult_d = 1.5
                        lost = False
                        new_form = True
                        key_push = False
                else:
                    if check_best(result):
                        end_menu = myfont2.render("Nouveau record : {}, bien joué !".format(result), False, pink)
                        screen.blit(end_menu, (75, 250))
                    else:
                        end_menu = myfont2.render("Tu as fait {}, bien joué !".format(result), False, pink)
                        screen.blit(end_menu, (50, 250))
            pg.display.update()


if __name__ == '__main__':
    main()
