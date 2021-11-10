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

        # load corresponding .ui file
        uic.loadUi('main-menu.ui', self)
        self.setWindowTitle("Wizard Tracker - Main Menu")

        # Only position matters, size is fixed in .ui
        self.setGeometry(1000, 500, 0, 0)

        # button functions
        btn_new_game = self.buttonNewGame
        btn_new_game.clicked.connect(self.start_new_game)
        btn_exit = self.buttonExit
        btn_exit.clicked.connect(self.close)

    # Opens new window to input player names
    def start_new_game(self):
        self.new_game = SetPlayers(self)
        self.new_game.show()
        self.close()


class SetPlayers(QMainWindow):
    """ Window for setting Player (count &) names and how many cards are used """

    def __init__(self, parent=None):
        super(SetPlayers, self).__init__()
        uic.loadUi('set-players.ui', self)
        self.setWindowTitle("Wizard Tracker - Set Players")
        self.setGeometry(1000, 400, 500, 450)  # TODO fixed size

        btn_start = self.buttonStartGame
        btn_start.clicked.connect(self.start_game)
        act_menu = self.actionMainMenu
        act_exit = self.actionExit

        # action menu functions
        act_menu.triggered.connect(self.menu)
        act_exit.triggered.connect(self.close)

    def start_game(self):
        """ Will check for sufficient inputs and create needed data for players """

        # get inputs from .ui form, convert to text/string and create list
        player_names = [self.le_name_p1.text(), self.le_name_p2.text(), self.le_name_p3.text(), self.le_name_p4.text()]

        # while "" in player_names: todo
        #     player_names.remove("")

        # if len(player_names) < 3:
        # check if all names are given, if not raise error
        if "" in player_names:
            error_msg("Please enter all players")

        else:
            # needed for non-standard player count, todo
            data.player_count = 4

            # set card count to given value, calculate rounds
            data.cards = self.inp_card_count.value()  # 60 is standard / min. With special game variants up to 75
            data.rounds = math.floor(data.cards / data.player_count)

            # create "Player" for each player and add to list
            for name in player_names:
                p = Player(name)
                player_data.append(p)

            # opens ui to start gameplay
            self.startgame = GameRound(self)
            self.startgame.show()
            self.close()

    # open main menu
    def menu(self):
        if self.close():
            self.menu = MainMenu()
            self.menu.show()

    # custom close event to ask for confirmation before closing so no data is lost by accident
    def closeEvent(self, event):

        # no confirmation needed if closed by "start game" button
        if self.sender() == self.buttonStartGame:
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
        self.setGeometry(1000, 400, 400, 450)  # TODO fixed size

        btn_next = self.buttonNext
        btn_next.clicked.connect(self.next_round)

        self.label_name_p1.setText(player_data[0].name)
        self.label_name_p2.setText(player_data[1].name)
        self.label_name_p3.setText(player_data[2].name)
        self.label_name_p4.setText(player_data[3].name)

        act_menu = self.actionMainMenu
        act_exit = self.actionExit
        act_menu.triggered.connect(self.menu)
        act_exit.triggered.connect(self.close)

        # refresh ui each round to show current round and expected input type
        self.refresh()

    def refresh(self):
        self.labelTitle.setText("Round: " + str(data.round_id) + " - " + str(data.type.name))

    def next_round(self):
        """ Check if inputs are valid and if so track data and move to next round """

        inputs = [self.inp_p1.value(), self.inp_p2.value(), self.inp_p3.value(), self.inp_p4.value()]

        # Check if input conforms to game rule: Amount of tricks != sum of predictions
        if sum(inputs) == data.round_id and data.type == Type.Prediction:
            error_msg("Sum can't be equal to round!")

        else:
            track_round(data, inputs)
            self.refresh()

            # detect when final round is played and show ending window
            if data.round_id > data.rounds:
                self.end = GameEnd()
                if self.close():
                    self.end.show()

    def menu(self):
        if self.close():
            self.menu = MainMenu()
            self.menu.show()

    # ask for confirmation before exiting
    def closeEvent(self, event):
        if self.sender() == self.buttonNext:
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

        menu = self.buttonMainMenu
        menu.clicked.connect(self.mainmenu)

        # ability to play new round with same players
        new_game = self.buttonNewRound
        new_game.clicked.connect(self.new_round)
        exit = self.buttonExit
        exit.clicked.connect(self.close)

        # display results of last round
        results = self.label_results
        output = ""

        # helper function for sorting
        def get_rank(player):
            return player.rank

        # sort players by their rank
        player_data.sort(key=get_rank)

        # generate results string
        for player in player_data:
            output = output + str(player) + '\n'

        # display results
        results.setText(output)

    def mainmenu(self):
        if self.close():
            # clear data of last game from memory
            player_data.clear()
            data.reset()

            self.menu = MainMenu()
            self.menu.show()

    def new_round(self):
        if self.close():
            # reset points and rank of players
            for player in player_data:
                player.points = 0
                player.rank = 0
            # start at round 1
            data.round_id = 1

            # launch into game
            self.new = GameRound()
            self.new.show()


# defines which type of input is expected
class Type(Enum):
    Prediction = 0
    Results = 1


@dataclass
class Player:
    """ Holds player data and provides tool for sorting and printing results """

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
    """ Holds game data, provide reset function """

    type: Type = Type.Prediction
    round_id: int = 1
    player_count: int = 4  # player count
    rounds: int = 15  # default for 4 players & 60 cards

    def __init__(self):
        self.reset()

    def reset(self):
        self.type = Type.Prediction
        self.round_id = 1
        self.player_count = 4
        self.rounds = 15


def track_round(data, inputs):
    """ write data from inputs, calculate round outcome and player points """

    # if Predictions are given save to player data
    if data.type == Type.Prediction:
        data.type = Type.Results
        i = 0
        for player in player_data:
            player.prediction = inputs[i]
            i += 1

    # results: calculate player points and save to player data
    elif data.type == Type.Results:
        data.type = Type.Prediction

        # needed to get players input from list
        i = 0
        for player in player_data:
            player.result = inputs[i]
            i += 1

            # calculate players points for right / wrong predictions and update player data
            if player.result == player.prediction:
                player.points += 20 + player.result * 10
            elif player.result != player.prediction:
                player.points -= 10 * abs(player.prediction - player.result)

        calculate_player_ranks(player_data)
        # move to next round
        data.round_id += 1


def calculate_player_ranks(player_data):
    """ Calculate and refresh players ranks """

    current_points = []
    current_points.clear()

    # put player points in ordered list
    for player in player_data:
        current_points.append(player.points)
    current_points.sort(reverse=True)

    # check players points against sorted list to calculate rank
    for player in player_data:
        i = 1
        for entry in current_points:
            if entry == player.points:
                player.rank = i
                break
            i += 1
        print(player)


def error_msg(message):
    """ Show error dialog with given message """
    msg = QMessageBox()
    msg.setText("Error")
    msg.setInformativeText(message)
    msg.setWindowTitle("Error")
    msg.setStyleSheet("QLabel{min-width: 300px;}")
    msg.exec_()


def main():
    """ Start app, init variables, show main menu """

    app = QApplication(sys.argv)
    mainmenu = MainMenu()
    mainmenu.show()
    global data, player_data
    data = GameData()
    player_data = []
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
