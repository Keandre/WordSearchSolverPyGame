import pygame, sys
from pygame.locals import * 
import colors
from word_search import WordSearch, WordMatch
pygame.init()

class Letter:
    def __init__(self, string, posx, posy):
        self.text = font.render(string, True, colors.BLACK, colors.WHITE)
        self.position = (posx, posy)

word_search = WordSearch('words.txt','wordsearch.txt')

WINDOWWIDTH, WINDOWHEIGHT = 600, 600
WINDOW_DIMENSIONS = (WINDOWWIDTH, WINDOWHEIGHT)
FPS = 30
fpsClock = pygame.time.Clock()
DISPLAYSURF = pygame.display.set_mode(WINDOW_DIMENSIONS, 0, 32)
font = pygame.font.Font('Anonymous.ttf', 20)
letters = []
XMARGIN = (WINDOWWIDTH / word_search.length_row) / 3
YMARGIN = (WINDOWHEIGHT / word_search.length) / 3

def convert_to_screen_coords(x, y):
    return XMARGIN + (WINDOWWIDTH / word_search.length_row) * x,  YMARGIN + (WINDOWHEIGHT / word_search.length) * y

for num, line in enumerate(word_search.word_search):
    for position, letter in enumerate(line):
        x, y = convert_to_screen_coords(position, num)
        l = Letter(letter, int(x), int(y))
        letters.append(l)

DISPLAYSURF.fill(colors.WHITE)
for letter in letters:
        DISPLAYSURF.blit(letter.text, letter.position)
word_search.draw(DISPLAYSURF, WINDOWWIDTH, WINDOWHEIGHT, XMARGIN, YMARGIN)

def main():
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
        fpsClock.tick(FPS)

main()