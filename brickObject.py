from movement import OneBlockForward, OneBlocktoRight, OneBlocktoLeft, OneBlockBehind
from ia import mov_HT

class HomemTosta:
    def __init__(self):
        self.coordinates = [0,0]
        self.direction = 'N'

    def getCoordinates(self):
        return self.coordinates

    def setDirection(self, value):
        return self.direction

    def getDirection(self):
        return self.direction

    def move(self):
        moveDecision = mov_HT(self.coordinates)
        

        if moveDecision[1] == 'N':
            self.goNorth()
        elif moveDecision[1] == 'S':
            self.goSouth()
        elif moveDecision[1] == 'E':
            self.goEast()
        elif moveDecision[1] == 'O':
            self.goWest()

        self.direction = moveDecision[1]
        self.coordinates = moveDecision[0]
        

    def goNorth(self):
        if self.direction == 'N':
            self.goForward()
        elif self.direction == 'S':
            self.goBackwards()
        elif self.direction == 'E':
            self.goLeft()
        elif self.direction == 'O':
            self.goRight()

        self.direction = 'N'
        
    def goSouth(self):
        if self.direction == 'N':
            self.goBackwards()
        elif self.direction == 'S':
            self.goForward()
        elif self.direction == 'E':
            self.goRight()
        elif self.direction == 'O':
            self.goLeft()

        self.direction = 'S'

    def goEast(self):
        if self.direction == 'N':
            self.goRight()
        elif self.direction == 'S':
            self.goLeft()
        elif self.direction == 'E':
            self.goForward()
        elif self.direction == 'O':
            self.goBackwards()

        self.direction = 'E'

    def goWest(self):
        if self.direction == 'N':
            self.goLeft()
        elif self.direction == 'S':
            self.goRight()
        elif self.direction == 'E':
            self.goBackwards()
        elif self.direction == 'O':
            self.goForward()

        self.direction == 'O'


    def goForward(self):
        OneBlockForward()

    def goRight(self):
        OneBlocktoRight()

    def goLeft(self):
        OneBlocktoLeft()

    def goBackwards(self):
        OneBlockBehind()

    def setCoordinates(self, value):
        self.coordinates = value
