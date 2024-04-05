from flask import Flask, render_template, redirect
from game import Game
from queue import Queue

mediator = Queue()
game = Game(mediator)
app = Flask(__name__)


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', game_state=game.game_state)


@app.route('/start', methods=['POST'])
def start():
    mediator.put('n')
    return redirect('/')


@app.route('/reset', methods=['POST'])
def reset():
    mediator.put('r')
    return redirect('/')


@app.route('/quit', methods=['POST'])
def stop():
    mediator.put('q')
    return redirect('/')


def main():
    game.start()
    app.run(debug=True)


if __name__ == "__main__":
    main()
