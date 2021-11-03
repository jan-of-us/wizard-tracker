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
        data.players = 4

        p1name = self.lineEdit.text()
        p2name = self.lineEdit_2.text()
        p3name = self.lineEdit_3.text()
        p4name = self.lineEdit_4.text()
        print(p1name, p2name)

        p1 = Player(p1name, 0, 0, 0, 0)
        p2 = Player(p2name, 0, 0, 0, 0)
        p3 = Player(p3name, 0, 0, 0, 0)
        p4 = Player(p4name, 0, 0, 0, 0)

        players.append(p1)
        players.append(p2)
        players.append(p3)
        players.append(p4)

        print(players)
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
        self.labelTitle.setText("Round: " + str(data.roundid) + " - " + str(data.type))
        self.label.setText(players[0].name)
        self.label_2.setText(players[1].name)
        self.label_3.setText(players[2].name)
        self.label_4.setText(players[3].name)

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
class Player:
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



data = GameData(Type.Prediction, 0, 0)
players = []

def main():
    app = QApplication(sys.argv)
    mainmenu = MainMenu()
    mainmenu.show()

    sys.exit(app.exec_())


if __name__ == "__main__":

    main()