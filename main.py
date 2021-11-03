from PyQt5.QtWidgets import *
from PyQt5.QtCore import pyqtSignal
from PyQt5 import uic
import sys
from dataclasses import dataclass, field
from enum import Enum, auto



class MainMenu(QMainWindow):
    def __init__(self, parent=None):
        super(MainMenu, self).__init__()
        uic.loadUi('main-menu.ui', self)
        self.setWindowTitle("Wizard Tracker - Main Menu")
        button = self.buttonNewGame
        button.clicked.connect(self.newGame)

    def newGame(self):
        self.newgame = SetPlayers(self)
        # self.newgame.closed.connect(self.show)
        self.newgame.show()
        self.close()

class SetPlayers(QMainWindow):

    closed = pyqtSignal()

    def __init__(self, parent=None):
        super(SetPlayers, self).__init__()
        uic.loadUi('set-players.ui', self)
        self.setWindowTitle("Wizard Tracker - Set Players")
        button = self.pushButton
        button.setText("Start")
        button.clicked.connect(self.startGame)

    def startGame(self):
        self.startgame = GameRound(self)
        # self.startgame.closed.connect(self.show)
        self.startgame.show()
        self.close()

    def closeEvent(self, event):
        self.closed.emit()
        event.accept()

class GameRound(QMainWindow):

    closed = pyqtSignal()

    def __init__(self, parent=None):
        super(GameRound, self).__init__()
        uic.loadUi('main-game-rounds.ui', self)
        button = self.pushButton
        button.setText("Next")
        button.clicked.connect(self.nextRound)

    def nextRound(self):
        self.setWindowTitle("Text")
        trackround(data)


    def closeEvent(self, event):
        self.closed.emit()
        event.accept()



class Type(Enum):
    Prediction = auto()
    Results = auto()

@dataclass
class Person:
    name: str
    points: int
    prediction: int
    result: int
    rank: int

    def __post_init__(self):
        self.sort_index = self.rank

    def __str__(self):
        return f'{self.name} has {self.points} points and is currently on rank {self.rank}'

@dataclass
class GameData:
    type: Type
    roundid: int = 0
    players: int = 0



def trackround(data):
    if data.type == Type.Prediction:
        data.type = Type.Results


    if data.type == Type.Results:
        data.type = Type.Prediction
    data.roundid += 1





def main():
    app = QApplication(sys.argv)
    mainmenu = MainMenu()
    mainmenu.show()
    data = GameData(0, Type.Prediction, 0)
    sys.exit(app.exec_())


if __name__ == "__main__":

    main()