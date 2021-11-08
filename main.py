import sys
import math
import sqlite3

from PyQt5.QtWidgets import *
from PyQt5.QtCore import pyqtSignal
from PyQt5 import uic
from dataclasses import dataclass
from enum import Enum


class MainMenu(QMainWindow):
    """ create main-menu ui and functions """

    def __init__(self, parent=None):
        super(MainMenu, self).__init__()
        uic.loadUi('main-menu.ui', self)
        self.setWindowTitle("Wizard Tracker - Main Menu")
        self.setGeometry(1000, 500, 0, 0)
        button = self.buttonNewGame
        button.clicked.connect(self.newGame)
        exit = self.buttonExit
        exit.clicked.connect(self.close)

    def newGame(self):
        self.newgame = SetPlayers(self)
        self.newgame.show()
        self.close()


class SetPlayers(QMainWindow):
    """ Window for setting Player count & names and how many cards are used """

    def __init__(self, parent=None):
        super(SetPlayers, self).__init__()
        uic.loadUi('set-players.ui', self)
        self.setWindowTitle("Wizard Tracker - Set Players")
        self.setGeometry(1000, 400, 500, 450)
        button = self.pushButton
        button.setText("Start")
        button.clicked.connect(self.startgame)
        menu = self.actionMainMenu
        exit = self.actionExit

        menu.triggered.connect(self.menu)
        exit.triggered.connect(self.close)

    def startgame(self):
        playernames = (self.lineEdit.text(), self.lineEdit_2.text(), self.lineEdit_3.text(), self.lineEdit_4.text())
        # playernames.remove("")

        if "" in playernames[0:3]:
            errormsg("Please enter playernames")

        else:
            data.players = 4  # TODO: Variable player count
            data.cards = 60  # 60 is standard / min. With special game variants up to ?  TODO: Set custom card count
            #data.rounds = math.floor(data.cards / data.players)

            for name in playernames:
                p = Player(name)
                print(p)
                players.append(p)



            print(players)
            self.startgame = GameRound(self)

            self.startgame.show()
            self.close()

    def menu(self):
        if self.close():
            self.menu = MainMenu()
            self.menu.show()


    def closeEvent(self, event):

        if self.sender() == self.pushButton:
            event.accept()
        else:
            msg = "Do you want to exit? All data will be lost!"
            reply = QMessageBox.question(self, 'Message', msg, QMessageBox.Yes, QMessageBox.No)
            if reply == QMessageBox.Yes:
                event.accept()
            else:
                event.ignore()

class GameRound(QMainWindow):
    """ Main Game Window - Track data of rounds, check for errors """

    def __init__(self, parent=None):
        super(GameRound, self).__init__()
        uic.loadUi('main-game-rounds.ui', self)
        self.setWindowTitle("Wizard Tracker")
        self.setGeometry(1000, 400, 400, 450)
        button = self.pushButton
        button.setText("Next")
        button.clicked.connect(self.nextround)
        self.label.setText(players[0].name)
        self.label_2.setText(players[1].name)
        self.label_3.setText(players[2].name)
        self.label_4.setText(players[3].name)
        menu = self.actionMainMenu
        exit = self.actionExit

        menu.triggered.connect(self.menu)
        exit.triggered.connect(self.close)
        self.refresh()

    def refresh(self):
        self.labelTitle.setText("Round: " + str(data.roundid) + " - " + str(data.type.name))

    def menu(self):
        if self.close():
            self.menu = MainMenu()
            self.menu.show()



    def nextround(self):
        """ Check if inputs are valid and if so track data and move to next """  # TODO: Descriptions

        inputs = [self.spinBox.value(), self.spinBox_2.value(), self.spinBox_3.value(), self.spinBox_4.value()]

        # Check if input conforms to game rule: Amount of tricks TODO: lookup "Stiche", != sum of predictions
        if sum(inputs) == data.roundid and data.type == Type.Prediction:
            errormsg("Sum can't be equal to round!")

        else:
            trackround(data, inputs)
            self.refresh()
            if data.roundid > data.rounds:
                print("End")  # TODO: end game
                self.end = GameEnd()
                if self.close():
                    self.end.show()



    def closeEvent(self, event):
        if self.sender() == self.pushButton:
            event.accept()
        else:
            msg = "Do you want to exit? All data will be lost!"
            reply = QMessageBox.question(self, 'Message', msg, QMessageBox.Yes, QMessageBox.No)
            if reply == QMessageBox.Yes:
                event.accept()
            else:
                event.ignore()

class GameEnd(QMainWindow):
    """ Display game results """

    def __init__(self, parent=None):
        super(GameEnd, self).__init__()
        uic.loadUi('game-finished.ui', self)
        self.setWindowTitle("Wizard Tracker - Game Results")
        self.setGeometry(1000, 500, 0, 0)
        button = self.buttonMainMenu
        #button.clicked.connect(self.newGame)
        exit = self.buttonExit
        exit.clicked.connect(self.close)
        results = self.label
        output = ""
        for player in players:
            output = output + str(player) + '\n'

        results.setText(output)



class Type(Enum):
    Prediction = 0
    Results = 1


@dataclass
class Player:
    name: str
    points: int = 0
    prediction: int = 0
    result: int = 0
    rank: int = 0

    def __post_init__(self):
        self.sort_index = self.rank

    def __str__(self):
        return f'{self.name} has {self.points} points and is currently on rank {self.rank}'

@dataclass
class GameData:
    type: Type = Type.Prediction
    roundid: int = 1
    players: int = 0  # player count
    rounds: int = 5 # default for 4 players & 60 cards TODO: changed for debugging


def trackround(data, inputs):

    if data.type == Type.Prediction:
        data.type = Type.Results
        print(sum(inputs))
        i = 0
        for player in players:
            player.prediction = inputs[i]
            i += 1
        print(players)

    elif data.type == Type.Results:
        data.type = Type.Prediction

        i = 0
        for player in players:
            player.result = inputs[i]
            i += 1
            if player.result == player.prediction:
                player.points += 20 + player.result * 10
            elif player.result != player.prediction:
                player.points -= 10 * abs(player.prediction - player.result)
            print(player)
        # playerranks(players)
        print(players)
        data.roundid += 1


data = GameData()
players = []

#def playerranks(players):
#    """ Checks rank of player and tracks in playerdata """
    # TODO


def errormsg(message):
    msg = QMessageBox()
    msg.setText("Error")
    msg.setInformativeText(message)
    msg.setWindowTitle("Error")
    msg.setStyleSheet("QLabel{min-width: 300px;}")
    msg.exec_()



def main():
    app = QApplication(sys.argv)
    mainmenu = MainMenu()
    mainmenu.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
