import dataclasses
import os
import signal
from queue import Queue
from threading import Thread
from time import sleep
from typing import Optional


# Holds the game state.  Flask will get this and use it to display things on the UI
@dataclasses.dataclass
class GameState:
    stage: Optional[str] = None
    game_running: bool = False


# Separate background thread to run the game independently of Flask.
class Game(Thread):
    _game_state: GameState

    @property
    def game_state(self) -> GameState:
        return self._game_state

    def __init__(self, mediator: Queue):
        super().__init__()
        self.mediator = mediator
        self._game_state = GameState(game_running=False)

    # Called when the Thread is started
    def run(self):
        # Game loop to run until 'q' is sent
        self.game_loop()

        # OS kill signal to shut down the Flask app
        os.kill(os.getpid(), signal.SIGINT)

    def game_loop(self):
        while True:
            next_command = self.mediator.get()

            if next_command == 'n':
                if not self._game_state.game_running:
                    self.new_game()
            if next_command == 'r':
                self._game_state = GameState()
            elif next_command == 'q':
                # break the loop
                return

    def new_game(self):
        self._game_state = GameState(game_running=True)

        self._game_state.stage = 'player1 turn'
        # Sleep and do nothing - pretend player 1 turn
        sleep(10)

        self._game_state.stage = 'player2 turn'
        # Sleep and do nothing - pretend player 2 turn
        sleep(10)

        self._game_state.stage = 'player1 wins'
