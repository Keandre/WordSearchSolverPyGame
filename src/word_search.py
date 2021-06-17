from typing import Match
import pygame 
import colors
from enum import Enum 

class MatchTypes(Enum):
    HORIZONTAL = 0
    HORIZONTAL_BACKWARDS = 1
    VERTICAL = 2
    VERTICAL_BACKWARDS = 3
    MAIN_DIAGONAL = 4
    MAIN_DIAGONAL_BACKWARDS = 5
    ANTI_DIAGONAL = 6
    ANTI_DIAGONAL_BACKWARDS = 7
    
class WordMatch:
    def __init__(self, x1, y1, x2, y2, match_type):
        self.first_letter_pos = (x1, y1)
        self.last_letter_pos = (x2, y2)
        self.match_type = match_type

    def valid(self):
        for x, y in zip(self.first_letter_pos, self.last_letter_pos):
            if x < 0 or y < 0:
                return False
        return True

class WordSearch:
    def __init__(self, words_file, wordsearch_file):
        self.words = []
        self.word_search = []
        
        for word in open(words_file, 'r').readlines():
            self.words.append(word.replace("\n","").replace(" ",""))
        
        for line in open(wordsearch_file, 'r').readlines():
            line = line.replace("\n", "")
            self.word_search.append(line)

        self.length = len(self.word_search)
        self.length_row = len(self.word_search[0])

        # Make sure that all the horizontal rows are all of the same llength
        for line in self.word_search:
            assert len(line) == self.length_row

        self.word_search_columns = ["".join(list(i)) for i in zip(*self.word_search)]

        self.diagonals = []
        self.antidiagonals = []
        
        #Generate diagonal self.words
        diagonal = ""
        for j in range(0, self.length):
            for i in range(self.length_row - 1, -1, -1):
                x, y = i, j
                while (x >= 0 and x < self.length_row) and (y >= 0 and y < self.length):
                   diagonal += self.word_search[y][x]
                   x, y = x + 1, y + 1
                self.diagonals.append(diagonal)
                diagonal = ""
            for i in range(0, self.length_row):
                x, y = i, j
                while (x >= 0 and x < self.length_row) and (y >= 0 and y < self.length):
                   diagonal += self.word_search[y][x]
                   x, y = x - 1, y + 1
                self.antidiagonals.append(diagonal)
                diagonal = ""

        self.matches = []
        
        #Find horizontal self.words
        for row, line in enumerate(self.word_search):
            for word in self.words:
                position = line.find(word)
                if position != -1:
                    match = WordMatch(position, row, position + len(word) - 1, row, MatchTypes.HORIZONTAL)
                    self.matches.append(match)
                position = line.find(word[::-1])
                if position != -1:
                    match = WordMatch(position + len(word) - 1, row, position, row, MatchTypes.HORIZONTAL_BACKWARDS)
                    self.matches.append(match)

        #Find vertical self.words
        for column, line in enumerate(self.word_search_columns):
            for word in self.words:
                position = line.find(word)
                if position != -1:
                    match = WordMatch(column, position, column, position + len(word) - 1, MatchTypes.VERTICAL)
                    self.matches.append(match)
                position = line.find(word[::-1])
                if position != -1:
                    match = WordMatch(column, position + len(word) - 1 , column, position, MatchTypes.VERTICAL_BACKWARDS)
                    self.matches.append(match)

        #Find main diagonal self.words
        for i in range(0, len(self.diagonals)):
            main = self.diagonals[i]
            for word in self.words:
                found = main.find(word)
                if found != -1:
                    x1 = (self.length_row - i - 1) + found 
                    y1 = found
                    x2 = (self.length_row - 1 - i) + found + len(word) - 1
                    y2 = found + len(word) - 1
                    match = WordMatch(x1, y1, x2, y2, MatchTypes.MAIN_DIAGONAL)
                    if match.valid():
                        self.matches.append(match)
                found = main.find(word[::-1])
                if found != -1:
                    x1 = (self.length_row - 1 - i) + found + len(word) - 1
                    y1 = found  + len(word) - 1
                    x2 = (self.length_row - i - 1) + found 
                    y2 = found
                    match = WordMatch(x1, y1, x2, y2, MatchTypes.MAIN_DIAGONAL_BACKWARDS)
                    if match.valid():
                        self.matches.append(match)

        #Find anti diagonal self.words
        for i in range(0, len(self.antidiagonals)):
            main = self.antidiagonals[i]
            for word in self.words:
                found = main.find(word)
                if found != -1:
                    x1 = i + found
                    y1 = found 
                    x2 = i - (len(word) - 1)   
                    y2 = found  + len(word) - 1
                    match = WordMatch(x1, y1, x2, y2, MatchTypes.ANTI_DIAGONAL)
                    self.matches.append(match)
                found = main.find(word[::-1])
                if found != -1:
                    x1 = i 
                    y1 = found  + len(word) - 1
                    x2 = i + found
                    y2 = found
                    match = WordMatch(x1, y1, x2, y2, MatchTypes.ANTI_DIAGONAL_BACKWARDS)
                    self.matches.append(match)

    def draw(self, screen, WINDOWWIDTH, WINDOWHEIGHT, XMARGIN, YMARGIN):
        def convert_for_drawing(x, y):
            return XMARGIN + (WINDOWWIDTH / self.length_row) * x,  YMARGIN + (WINDOWHEIGHT / self.length) * y 

        XLINEMARGIN, YLINEMARGIN = 6, 6 
        for match in self.matches:
            x1, y1 = convert_for_drawing(match.first_letter_pos[0], match.first_letter_pos[1])
            x2, y2 = convert_for_drawing(match.last_letter_pos[0], match.last_letter_pos[1])
            if match.match_type == MatchTypes.HORIZONTAL:
                y1 += YLINEMARGIN
                y2 += YLINEMARGIN
                x2 += XLINEMARGIN
            if match.match_type == MatchTypes.HORIZONTAL_BACKWARDS:
                y1 += YLINEMARGIN
                y2 += YLINEMARGIN
                x1 += XLINEMARGIN
            if match.match_type == MatchTypes.VERTICAL:
                x1 += XLINEMARGIN
                x2 += XLINEMARGIN
                y2 += YLINEMARGIN * 2.5 
            if match.match_type == MatchTypes.VERTICAL_BACKWARDS:
                x1 += XLINEMARGIN
                x2 += XLINEMARGIN
                y1 += YLINEMARGIN * 2.5 
            if match.match_type == MatchTypes.MAIN_DIAGONAL:
                x2 += XLINEMARGIN * 2.5
                y2 += YLINEMARGIN * 2.5
            if match.match_type == MatchTypes.MAIN_DIAGONAL_BACKWARDS:
                x1 += XLINEMARGIN * 2.5
                y1 += YLINEMARGIN * 2.5
            if match.match_type in (MatchTypes.ANTI_DIAGONAL, MatchTypes.ANTI_DIAGONAL_BACKWARDS):
                x1 += XLINEMARGIN
                x2 += XLINEMARGIN 
                y1 += YLINEMARGIN
                y2 += YLINEMARGIN 
            pygame.draw.line(screen, colors.RED, (x1, y1), (x2, y2))
            pygame.display.update()